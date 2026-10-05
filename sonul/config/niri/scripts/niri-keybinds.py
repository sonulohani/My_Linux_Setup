#!/usr/bin/env python3
"""Searchable overlay of niri key bindings.

niri's IPC has no request that lists binds, so the config is parsed directly,
following `include` directives from the main config file. Section headers are
taken from decorated comments inside `binds {}`, e.g. `// ─── Media ───`.

    niri-keybinds.py                 toggle the overlay
    niri-keybinds.py --list          print the bindings to the terminal
    niri-keybinds.py --config FILE   read FILE instead of the niri config
"""

from __future__ import annotations

import argparse
import bisect
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from typing import NamedTuple

APP_ID = "niri.keybinds.Overlay"
LAYER_NAMESPACE = "niri-keybinds"


# ───────────────────────────── KDL parser ─────────────────────────────
# Minimal parser covering both KDL v1 and v2 syntax as used by niri configs.

NEWLINES = "\n\r\x0b\x0c\x85\u2028\u2029"
NEWLINE_RE = re.compile(r"\r\n|[\n\r\x0b\x0c\x85\u2028\u2029]")
IDENT_STOP = frozenset(" \t\ufeff{}()[];=\"\\/" + NEWLINES)
ESCAPES = {"n": "\n", "r": "\r", "t": "\t", "\\": "\\", "/": "/", '"': '"',
           "b": "\b", "f": "\f", "s": " "}
UNICODE_ESCAPE_RE = re.compile(r"\\u\{([0-9a-fA-F]{1,6})\}")


class KdlError(Exception):
    pass


class Node:
    __slots__ = ("name", "args", "props", "children", "line", "end_line")

    def __init__(self, name: str, line: int):
        self.name = name
        self.args: list = []
        self.props: dict = {}
        self.children: list[Node] = []
        self.line = line
        self.end_line = line


class Comment(NamedTuple):
    line: int
    text: str
    trailing: bool  # code precedes the comment on the same line


def _unescape(s: str) -> str:
    def repl(m: re.Match) -> str:
        e = m.group(1)
        if e[0] == "u":
            return chr(int(e[2:-1], 16))
        if e[0].isspace():
            return ""
        return ESCAPES.get(e, e)
    return re.sub(r"\\(u\{[0-9a-fA-F]{1,6}\}|\s+|.)", repl, s)


def _dedent(s: str) -> str:
    lines = NEWLINE_RE.split(s)
    if len(lines) < 2:
        return s
    lines = lines[1:]
    indent = lines.pop() if not lines[-1].strip() else ""
    return "\n".join(l[len(indent):] if l.startswith(indent) else l.lstrip() for l in lines)


class KdlParser:
    def __init__(self, text: str, filename: str = "<string>"):
        self.text = text
        self.filename = filename
        self.pos = 0
        self.comments: list[Comment] = []
        self._line_starts = [0] + [m.end() for m in NEWLINE_RE.finditer(text)]

    def line_at(self, pos: int) -> int:
        return bisect.bisect_right(self._line_starts, pos)

    def error(self, msg: str) -> KdlError:
        return KdlError(f"{self.filename}:{self.line_at(self.pos)}: {msg}")

    def parse(self) -> list[Node]:
        if self.text.startswith("\ufeff"):
            self.pos = 1
        return self._nodes(top=True)

    def _peek(self, offset: int = 0) -> str:
        i = self.pos + offset
        return self.text[i] if i < len(self.text) else ""

    # ── whitespace & comments ──

    def _skip_line_comment(self) -> None:
        start = self.pos
        line = self.line_at(start)
        trailing = bool(self.text[self._line_starts[line - 1]:start].strip())
        end = start
        while end < len(self.text) and self.text[end] not in NEWLINES:
            end += 1
        self.comments.append(Comment(line, self.text[start + 2:end].strip(), trailing))
        self.pos = end

    def _skip_block_comment(self) -> None:
        depth = 0
        while self.pos < len(self.text):
            if self.text.startswith("/*", self.pos):
                depth += 1
                self.pos += 2
            elif self.text.startswith("*/", self.pos):
                depth -= 1
                self.pos += 2
                if depth == 0:
                    return
            else:
                self.pos += 1
        raise self.error("unterminated block comment")

    def _consume_newline(self) -> None:
        if self.text.startswith("\r\n", self.pos):
            self.pos += 2
        elif self.pos < len(self.text) and self.text[self.pos] in NEWLINES:
            self.pos += 1

    def _skip_inline_ws(self) -> None:
        """Skip spaces, block comments and line continuations, but not newlines."""
        while self.pos < len(self.text):
            c = self.text[self.pos]
            if c in NEWLINES:
                return
            if c.isspace() or c == "\ufeff":
                self.pos += 1
            elif self.text.startswith("/*", self.pos):
                self._skip_block_comment()
            elif c == "\\":
                self.pos += 1
                while self._peek() and self._peek() not in NEWLINES and self._peek().isspace():
                    self.pos += 1
                if self.text.startswith("//", self.pos):
                    self._skip_line_comment()
                self._consume_newline()
            else:
                return

    def _skip_ws_nl(self) -> None:
        """Skip everything that may appear between nodes."""
        while self.pos < len(self.text):
            c = self.text[self.pos]
            if c.isspace() or c in ";\ufeff":
                self.pos += 1
            elif self.text.startswith("//", self.pos):
                self._skip_line_comment()
            elif self.text.startswith("/*", self.pos):
                self._skip_block_comment()
            elif c == "\\":
                self._skip_inline_ws()
            else:
                return

    def _skip_type_annotation(self) -> None:
        if self._peek() == "(":
            end = self.text.find(")", self.pos)
            if end < 0:
                raise self.error("unterminated type annotation")
            self.pos = end + 1
            self._skip_inline_ws()

    # ── structure ──

    def _nodes(self, top: bool) -> list[Node]:
        nodes = []
        while True:
            self._skip_ws_nl()
            if self.pos >= len(self.text):
                if top:
                    return nodes
                raise self.error("unexpected end of file, missing '}'")
            if self.text[self.pos] == "}":
                if top:
                    raise self.error("unexpected '}'")
                self.pos += 1
                return nodes
            discard = False
            if self.text.startswith("/-", self.pos):
                self.pos += 2
                self._skip_ws_nl()
                discard = True
            node = self._node()
            if not discard:
                nodes.append(node)

    def _node(self) -> Node:
        line = self.line_at(self.pos)
        self._skip_type_annotation()
        name, _ = self._token()
        node = Node(name, line)
        while True:
            self._skip_inline_ws()
            if self.pos >= len(self.text):
                break
            c = self.text[self.pos]
            if c == ";":
                self.pos += 1
                break
            if c in NEWLINES:
                self._consume_newline()
                break
            if self.text.startswith("//", self.pos):
                self._skip_line_comment()
                continue
            if c == "}":
                break
            discard = False
            if self.text.startswith("/-", self.pos):
                self.pos += 2
                self._skip_inline_ws()
                discard = True
            if self._peek() == "{":
                self.pos += 1
                children = self._nodes(top=False)
                if not discard:
                    node.children.extend(children)
                continue
            self._skip_type_annotation()
            tok, is_string = self._token()
            after_token = self.pos
            self._skip_inline_ws()
            if self._peek() == "=":
                self.pos += 1
                self._skip_inline_ws()
                self._skip_type_annotation()
                value = self._value(*self._token())
                if not discard:
                    node.props[tok] = value
            else:
                self.pos = after_token
                if not discard:
                    node.args.append(self._value(tok, is_string))
        node.end_line = self.line_at(max(self.pos - 1, 0))
        return node

    # ── tokens ──

    def _token(self) -> tuple[str, bool]:
        """Read a string or a bare token, returning (text, is_string)."""
        t, p = self.text, self.pos
        c = self._peek()
        if c == '"':
            if t.startswith('"""', p):
                return self._multiline_string(), True
            return self._quoted_string(), True
        if c in ("r", "#"):
            j = p + 1 if c == "r" else p
            while j < len(t) and t[j] == "#":
                j += 1
            if j < len(t) and t[j] == '"' and (c == "#" or j > p):
                self.pos = p + 1 if c == "r" else p
                return self._raw_string(), True
        start = p
        while self.pos < len(t) and t[self.pos] not in IDENT_STOP:
            self.pos += 1
        if self.pos == start:
            raise self.error(f"unexpected character {t[start]!r}" if start < len(t)
                             else "unexpected end of file")
        return t[start:self.pos], False

    def _quoted_string(self) -> str:
        t = self.text
        self.pos += 1
        out = []
        while True:
            if self.pos >= len(t):
                raise self.error("unterminated string")
            c = t[self.pos]
            if c == '"':
                self.pos += 1
                return "".join(out)
            if c != "\\":
                out.append(c)
                self.pos += 1
                continue
            nxt = t[self.pos + 1:self.pos + 2]
            if nxt in ESCAPES:
                out.append(ESCAPES[nxt])
                self.pos += 2
            elif nxt == "u":
                m = UNICODE_ESCAPE_RE.match(t, self.pos)
                if not m:
                    raise self.error("invalid unicode escape")
                out.append(chr(int(m.group(1), 16)))
                self.pos = m.end()
            elif nxt.isspace():
                self.pos += 1
                while self.pos < len(t) and t[self.pos].isspace():
                    self.pos += 1
            else:
                raise self.error(f"invalid escape '\\{nxt}'")

    def _multiline_string(self) -> str:
        t = self.text
        self.pos += 3
        start = self.pos
        while not t.startswith('"""', self.pos):
            if self.pos >= len(t):
                raise self.error("unterminated multi-line string")
            self.pos += 2 if t[self.pos] == "\\" else 1
        raw = t[start:self.pos]
        self.pos += 3
        return _unescape(_dedent(raw))

    def _raw_string(self) -> str:
        t = self.text
        hashes = 0
        while t[self.pos] == "#":
            hashes += 1
            self.pos += 1
        quote = '"""' if t.startswith('"""', self.pos) else '"'
        self.pos += len(quote)
        close = quote + "#" * hashes
        end = t.find(close, self.pos)
        if end < 0:
            raise self.error("unterminated raw string")
        s = t[self.pos:end]
        self.pos = end + len(close)
        return _dedent(s) if quote == '"""' else s

    @staticmethod
    def _value(tok: str, is_string: bool):
        if is_string:
            return tok
        if tok in ("true", "#true"):
            return True
        if tok in ("false", "#false"):
            return False
        if tok in ("null", "#null"):
            return None
        num = tok.replace("_", "")
        for pattern, base in ((r"[+-]?0x[0-9a-fA-F]+", 16), (r"[+-]?0o[0-7]+", 8),
                              (r"[+-]?0b[01]+", 2), (r"[+-]?\d+", 10)):
            if re.fullmatch(pattern, num):
                return int(num, base)
        if re.fullmatch(r"[+-]?\d+(\.\d+)?([eE][+-]?\d+)?", num):
            return float(num)
        return tok


# ──────────────────────────── niri bindings ────────────────────────────

MOD_ALIASES = {
    "ctrl": "Ctrl", "control": "Ctrl", "shift": "Shift", "alt": "Alt",
    "super": "Super", "win": "Super", "iso_level3_shift": "AltGr", "mod5": "AltGr",
    "iso_level5_shift": "Level5",
}
MOD_ORDER = ["Super", "Ctrl", "Alt", "Shift", "AltGr", "Level5"]
MOD_KEY_NAMES = {"super": "Super", "alt": "Alt", "ctrl": "Ctrl", "shift": "Shift",
                 "isolevel3shift": "AltGr", "isolevel5shift": "Level5"}

KEY_LABELS = {
    "slash": "/", "backslash": "\\", "bracketleft": "[", "bracketright": "]",
    "braceleft": "{", "braceright": "}", "parenleft": "(", "parenright": ")",
    "comma": ",", "period": ".", "minus": "-", "equal": "=", "plus": "+",
    "semicolon": ";", "colon": ":", "apostrophe": "'", "quotedbl": '"', "grave": "`",
    "asciitilde": "~", "less": "<", "greater": ">", "question": "?",
    "space": "Space", "return": "Enter", "kp_enter": "Num Enter", "escape": "Esc",
    "tab": "Tab", "iso_left_tab": "Tab", "backspace": "Backspace", "delete": "Del",
    "insert": "Ins", "home": "Home", "end": "End", "page_up": "PgUp", "prior": "PgUp",
    "page_down": "PgDn", "next": "PgDn", "left": "←", "right": "→", "up": "↑",
    "down": "↓", "print": "PrtSc", "pause": "Pause", "scroll_lock": "ScrLk",
    "caps_lock": "Caps", "num_lock": "NumLk", "menu": "Menu",
    "wheelscrollup": "Wheel ↑", "wheelscrolldown": "Wheel ↓",
    "wheelscrollleft": "Wheel ←", "wheelscrollright": "Wheel →",
    "touchpadscrollup": "Touchpad ↑", "touchpadscrolldown": "Touchpad ↓",
    "touchpadscrollleft": "Touchpad ←", "touchpadscrollright": "Touchpad →",
    "mouseleft": "Left Click", "mouseright": "Right Click", "mousemiddle": "Middle Click",
    "mouseback": "Mouse Back", "mouseforward": "Mouse Forward",
    "xf86audioraisevolume": "Volume +", "xf86audiolowervolume": "Volume −",
    "xf86audiomute": "Mute", "xf86audiomicmute": "Mic Mute",
    "xf86audionext": "Next Track", "xf86audioprev": "Prev Track",
    "xf86audioplay": "Play", "xf86audiopause": "Pause", "xf86audiostop": "Stop",
    "xf86monbrightnessup": "Brightness +", "xf86monbrightnessdown": "Brightness −",
    "xf86kbdbrightnessup": "Kbd Light +", "xf86kbdbrightnessdown": "Kbd Light −",
}

DECOR = "─━═—–\\-=#*~"
SECTION_RE = re.compile(rf"^[{DECOR}]{{2,}}\s*(.*?\w.*?)\s*[{DECOR}]{{2,}}$")


@dataclass
class Bind:
    combo: str
    mods: list[str]
    key: str
    title: str
    custom_title: bool
    action: str
    flags: list[str]
    note: str
    section: str
    file: str
    line: int

    @property
    def keys_text(self) -> str:
        return " + ".join(self.mods + [self.key])

    @property
    def haystack(self) -> str:
        return " ".join([self.combo, self.keys_text, self.title, self.action,
                         self.section, self.note, *self.flags]).lower()


@dataclass
class Keymap:
    binds: list[Bind] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error: str | None = None


def key_label(key: str) -> str:
    low = key.lower()
    if low in KEY_LABELS:
        return KEY_LABELS[low]
    if len(key) == 1:
        return key.upper()
    if low.startswith("xf86"):
        return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", key[4:]) or key
    if low.startswith("kp_"):
        return "Num " + key_label(key[3:])
    return key[:1].upper() + key[1:]


def parse_combo(combo: str, mod_name: str) -> tuple[list[str], str, str]:
    """Return (display modifiers, display key, raw key) for e.g. 'Mod+Shift+Slash'."""
    *mods, key = combo.split("+")
    names: list[str] = []
    for m in mods:
        name = mod_name if m.lower() == "mod" else MOD_ALIASES.get(m.lower(), m)
        if name not in names:
            names.append(name)
    names.sort(key=lambda n: MOD_ORDER.index(n) if n in MOD_ORDER else len(MOD_ORDER))
    return names, key_label(key), key


def kdl_value(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, str):
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return str(v)


def plain_value(v) -> str:
    return v if isinstance(v, str) else kdl_value(v)


def format_action(node: Node) -> str:
    parts = [node.name, *map(kdl_value, node.args),
             *(f"{k}={kdl_value(v)}" for k, v in node.props.items())]
    if node.children:
        parts.append("{ … }")
    return " ".join(parts)


def describe_action(node: Node) -> str:
    args = [plain_value(a) for a in node.args]
    if node.name in ("spawn", "spawn-sh"):
        return "Run " + " ".join(args) if args else "Run command"
    text = node.name.replace("-", " ").capitalize()
    if args:
        text += " " + " ".join(args)
    extras = [k.replace("-", " ") if v is True else f"{k.replace('-', ' ')}: {plain_value(v)}"
              for k, v in node.props.items()]
    if extras:
        text += f" ({', '.join(extras)})"
    return text


def auto_section(action: str) -> str:
    if action.startswith("spawn"):
        return "Applications"
    if "screenshot" in action:
        return "Screenshots"
    if "workspace" in action:
        return "Workspaces"
    if "monitor" in action:
        return "Monitors"
    if action.startswith("focus-"):
        return "Focus"
    if action.startswith("move-"):
        return "Move"
    if any(w in action for w in ("width", "height", "maximize", "fullscreen", "floating",
                                 "tabbed", "center", "consume", "expel", "column")):
        return "Layout"
    return "General"


def bind_flags(props: dict) -> list[str]:
    flags = []
    if props.get("allow-when-locked") is True:
        flags.append("works when locked")
    if props.get("repeat") is False:
        flags.append("no repeat")
    if "cooldown-ms" in props:
        flags.append(f"{props['cooldown-ms']} ms cooldown")
    if props.get("allow-inhibiting") is False:
        flags.append("not inhibitable")
    return flags


def section_headers(comments: list[Comment], block: Node) -> list[tuple[int, str]]:
    headers = []
    for c in comments:
        if block.line < c.line < block.end_line and not c.trailing:
            m = SECTION_RE.match(c.text)
            if m:
                headers.append((c.line, m.group(1)))
    return headers


def default_config_path() -> str:
    candidates = []
    if os.environ.get("NIRI_CONFIG"):
        candidates.append(os.environ["NIRI_CONFIG"])
    config_home = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    candidates += [os.path.join(config_home, "niri", "config.kdl"), "/etc/niri/config.kdl"]
    return next((c for c in candidates if os.path.isfile(c)), candidates[0])


def load_keymap(path: str) -> Keymap:
    km = Keymap()
    blocks: list[tuple[str, Node, list[Comment]]] = []
    mod_name = "Super"
    stack: list[str] = []

    def visit(file: str) -> None:
        nonlocal mod_name
        real = os.path.realpath(file)
        if real in stack:
            km.warnings.append(f"include cycle ignored: {file}")
            return
        with open(file, encoding="utf-8") as f:
            parser = KdlParser(f.read(), file)
        nodes = parser.parse()
        km.files.append(file)
        stack.append(real)
        for node in nodes:
            if node.name == "include" and node.args:
                inc = os.path.normpath(os.path.join(
                    os.path.dirname(file), os.path.expanduser(str(node.args[0]))))
                if os.path.isfile(inc):
                    visit(inc)
                elif not node.props.get("optional"):
                    km.warnings.append(f"included file not found: {inc}")
            elif node.name == "binds":
                blocks.append((file, node, parser.comments))
            elif node.name == "input":
                for child in node.children:
                    if child.name == "mod-key" and child.args:
                        raw = str(child.args[0])
                        mod_name = MOD_KEY_NAMES.get(raw.lower().replace("_", ""), raw)
        stack.pop()

    try:
        visit(path)
    except (OSError, UnicodeDecodeError, KdlError) as e:
        km.error = str(e)
        return km

    use_headers = any(section_headers(c, b) for _, b, c in blocks)
    by_combo: dict[tuple, int] = {}
    binds: list[Bind | None] = []
    for file, block, comments in blocks:
        headers = section_headers(comments, block)
        notes = {c.line: c.text for c in comments if c.trailing}
        for node in block.children:
            if not node.children:
                continue
            action = node.children[0]
            section = None
            for line, title in headers:
                if line >= node.line:
                    break
                section = title
            if section is None:
                section = "General" if use_headers else auto_section(action.name)
            note = next((notes[l] for l in range(node.line, node.end_line + 1) if l in notes), "")
            mods, key, raw_key = parse_combo(node.name, mod_name)
            title = node.props.get("hotkey-overlay-title")
            custom = isinstance(title, str) and bool(title.strip())
            bind = Bind(
                combo=node.name, mods=mods, key=key,
                title=title.strip() if custom else describe_action(action),
                custom_title=custom, action=format_action(action),
                flags=bind_flags(node.props), note=note, section=section,
                file=file, line=node.line,
            )
            # A later definition of the same combo overrides the earlier one, like in niri.
            ident = (frozenset(mods), raw_key.lower())
            if ident in by_combo:
                binds[by_combo[ident]] = None
            by_combo[ident] = len(binds)
            binds.append(bind)
    km.binds = [b for b in binds if b is not None]
    return km


def group_binds(binds: list[Bind]) -> list[tuple[str, list[Bind]]]:
    groups: dict[str, list[Bind]] = {}
    for b in binds:
        groups.setdefault(b.section, []).append(b)
    return list(groups.items())


def linear_partition(weights: list[float], k: int) -> list[list[int]]:
    """Split item indices into k contiguous runs minimising the heaviest run."""
    n = len(weights)
    k = max(1, min(k, n))
    if n == 0:
        return []
    prefix = [0.0]
    for w in weights:
        prefix.append(prefix[-1] + w)
    inf = float("inf")
    best = [[inf] * (n + 1) for _ in range(k + 1)]
    cut = [[0] * (n + 1) for _ in range(k + 1)]
    best[0][0] = 0.0
    for j in range(1, k + 1):
        for i in range(j, n + 1):
            for p in range(j - 1, i):
                cost = max(best[j - 1][p], prefix[i] - prefix[p])
                if cost < best[j][i]:
                    best[j][i], cut[j][i] = cost, p
    runs, i = [], n
    for j in range(k, 0, -1):
        p = cut[j][i]
        runs.append(list(range(p, i)))
        i = p
    return runs[::-1]


def shorten_home(path: str) -> str:
    home = os.path.expanduser("~")
    return "~" + path[len(home):] if path.startswith(home + os.sep) else path


# ─────────────────────────────── theme ───────────────────────────────

def load_theme_colors() -> dict[str, str]:
    """Read literal @define-color values from the GTK4 user theme (e.g. Noctalia's)."""
    colors: dict[str, str] = {}
    base = os.path.join(os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config"),
                        "gtk-4.0")
    for name in ("colors.css", "gtk.css", "noctalia.css"):
        try:
            with open(os.path.join(base, name), encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        for m in re.finditer(r"@define-color\s+([\w-]+)\s+(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))\s*;",
                             text):
            colors[m.group(1)] = m.group(2)
    return colors


def parse_rgb(color: str | None, fallback: tuple[int, int, int]) -> tuple[int, int, int]:
    color = (color or "").strip()
    if m := re.fullmatch(r"#([0-9a-fA-F]{6})(?:[0-9a-fA-F]{2})?", color):
        h = m.group(1)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if m := re.fullmatch(r"#([0-9a-fA-F]{3})", color):
        return tuple(int(c * 2, 16) for c in m.group(1))  # type: ignore[return-value]
    if m := re.fullmatch(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+).*\)", color):
        return tuple(int(x) for x in m.groups())  # type: ignore[return-value]
    return fallback


CSS_TEMPLATE = """
window.niri-keybinds { background: none; background-color: transparent; }
.nk-backdrop { background-color: rgba(0, 0, 0, 0.42); }
.nk-card {
  background-color: %(card)s;
  color: %(fg)s;
  border: 1px solid %(outline)s;
  border-radius: 22px;
  padding: 22px 26px 14px 26px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.45);
}
.nk-title { font-size: 19pt; font-weight: 800; }
.nk-subtle { color: %(muted)s; }
.nk-search {
  min-height: 34px;
  min-width: 380px;
  padding: 0 10px;
  border-radius: 12px;
  border: 1px solid %(outline)s;
  background-color: %(surface)s;
  color: %(fg)s;
  outline: none;
  box-shadow: none;
}
.nk-search:focus-within { border-color: %(accent)s; }
.nk-section-head { border-bottom: 1px solid %(outline)s; padding: 0 8px 6px 8px; margin-bottom: 4px; }
.nk-section-title { color: %(accent)s; font-weight: 800; font-size: 9.5pt; letter-spacing: 1px; }
.nk-section-count { color: %(muted)s; font-size: 9pt; }
.nk-row { padding: 5px 8px; border-radius: 10px; }
.nk-row:hover { background-color: %(hover)s; }
.nk-bind-detail { color: %(muted)s; font-size: 8.5pt; }
.nk-key {
  min-width: 14px;
  padding: 1px 7px;
  border-radius: 7px;
  border: 1px solid %(key_border)s;
  border-bottom-width: 3px;
  background-color: %(surface)s;
  color: %(fg)s;
  font-weight: 700;
  font-size: 9pt;
}
.nk-key.nk-mod { color: %(accent)s; }
.nk-plus { color: %(muted)s; font-size: 8pt; }
.nk-footer { color: %(muted)s; font-size: 9pt; }
.nk-empty { color: %(muted)s; font-size: 13pt; }
.nk-error { color: %(error)s; font-family: monospace; }
"""


def build_css() -> str:
    c = load_theme_colors()
    bg = parse_rgb(c.get("window_bg_color"), (18, 22, 28))
    fg = parse_rgb(c.get("window_fg_color"), (226, 226, 230))
    surface = parse_rgb(c.get("card_bg_color") or c.get("popover_bg_color"), (32, 36, 44))
    accent = parse_rgb(c.get("accent_color") or c.get("accent_bg_color"), (138, 180, 248))
    error = parse_rgb(c.get("error_bg_color") or c.get("destructive_bg_color"), (255, 180, 171))

    def rgba(rgb: tuple[int, int, int], a: float = 1.0) -> str:
        return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {a})"

    return CSS_TEMPLATE % {
        "card": rgba(bg, 0.97), "fg": rgba(fg), "surface": rgba(surface),
        "accent": rgba(accent), "error": rgba(error), "outline": rgba(fg, 0.10),
        "key_border": rgba(fg, 0.16), "muted": rgba(fg, 0.58), "hover": rgba(fg, 0.06),
    }


# ──────────────────────────────── GUI ────────────────────────────────

Gtk = Gdk = Pango = GLib = LayerShell = None


def load_gtk() -> None:
    global Gtk, Gdk, Pango, GLib, LayerShell
    from ctypes import CDLL
    # gtk4-layer-shell has to be loaded before libwayland-client, i.e. before GTK.
    for lib in ("libgtk4-layer-shell.so.0", "libgtk4-layer-shell.so"):
        try:
            CDLL(lib)
            break
        except OSError:
            pass
    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version("Gdk", "4.0")
    gi.require_version("Pango", "1.0")
    from gi.repository import Gdk, GLib, Gtk, Pango
    try:
        gi.require_version("Gtk4LayerShell", "1.0")
        from gi.repository import Gtk4LayerShell as LayerShell
    except (ImportError, ValueError):
        LayerShell = None


def focused_output_name() -> str | None:
    try:
        out = subprocess.run(["niri", "msg", "--json", "focused-output"],
                             capture_output=True, text=True, timeout=1)
        return json.loads(out.stdout).get("name")
    except (OSError, ValueError, AttributeError, subprocess.SubprocessError):
        return None


def focused_monitor(display):
    monitors = display.get_monitors()
    items = [monitors.get_item(i) for i in range(monitors.get_n_items())]
    name = focused_output_name()
    for m in items:
        if name and m.get_connector() == name:
            return m
    return items[0] if items else None


class Section:
    def __init__(self, box, count_label, rows):
        self.box = box
        self.count_label = count_label
        self.rows = rows  # [(widget, haystack, weight)]
        self.visible_weight = 0.0
        self.visible_rows = len(rows)


class Overlay:
    def __init__(self, app, keymap: Keymap, config_path: str):
        self.keymap = keymap
        self.sections: list[Section] = []
        self.total = len(keymap.binds)

        display = Gdk.Display.get_default()
        provider = Gtk.CssProvider()
        css = build_css()
        if hasattr(provider, "load_from_string"):
            provider.load_from_string(css)
        else:
            provider.load_from_data(css, -1)
        Gtk.StyleContext.add_provider_for_display(
            display, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)

        monitor = focused_monitor(display)
        geo = monitor.get_geometry() if monitor else None
        mon_w, mon_h = (geo.width, geo.height) if geo else (1600, 900)

        self.win = Gtk.Window(application=app, title="Niri Keybindings")
        self.win.add_css_class("niri-keybinds")
        if LayerShell is not None and LayerShell.is_supported():
            LayerShell.init_for_window(self.win)
            LayerShell.set_namespace(self.win, LAYER_NAMESPACE)
            LayerShell.set_layer(self.win, LayerShell.Layer.OVERLAY)
            LayerShell.set_keyboard_mode(self.win, LayerShell.KeyboardMode.EXCLUSIVE)
            LayerShell.set_exclusive_zone(self.win, -1)
            for edge in (LayerShell.Edge.TOP, LayerShell.Edge.BOTTOM,
                         LayerShell.Edge.LEFT, LayerShell.Edge.RIGHT):
                LayerShell.set_anchor(self.win, edge, True)
            if monitor is not None:
                LayerShell.set_monitor(self.win, monitor)
        else:
            self.win.set_decorated(False)
            self.win.fullscreen()

        margin_x = max(24, (mon_w - 1760) // 2)
        margin_y = max(24, int(mon_h * 0.05))
        card_w = mon_w - 2 * margin_x
        ncols = max(1, min(4, (card_w - 52) // 470))

        self.backdrop = Gtk.Box()
        self.backdrop.add_css_class("nk-backdrop")
        self.card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14,
                            hexpand=True, vexpand=True)
        self.card.add_css_class("nk-card")
        self.card.set_margin_start(margin_x)
        self.card.set_margin_end(margin_x)
        self.card.set_margin_top(margin_y)
        self.card.set_margin_bottom(margin_y)
        self.backdrop.append(self.card)
        self.win.set_child(self.backdrop)

        # Header
        header = Gtk.Box(spacing=14)
        title = Gtk.Label(label="Keybindings", xalign=0, valign=Gtk.Align.CENTER)
        title.add_css_class("nk-title")
        self.count = Gtk.Label(xalign=0, valign=Gtk.Align.CENTER, hexpand=True)
        self.count.add_css_class("nk-subtle")
        self.search = Gtk.SearchEntry(placeholder_text="Search keys, actions, commands…",
                                      valign=Gtk.Align.CENTER)
        self.search.add_css_class("nk-search")
        if hasattr(self.search, "set_search_delay"):
            self.search.set_search_delay(0)
        self.search.set_key_capture_widget(self.win)
        self.search.connect("search-changed", self._apply_filter)
        header.append(title)
        header.append(self.count)
        header.append(self.search)
        self.card.append(header)

        # Body
        self.columns_box = Gtk.Box(spacing=32, homogeneous=True)
        self.columns_box.set_margin_end(10)
        self.columns = []
        for _ in range(ncols):
            col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20, valign=Gtk.Align.START)
            self.columns_box.append(col)
            self.columns.append(col)
        self.scroller = Gtk.ScrolledWindow(vexpand=True)
        self.scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroller.set_child(self.columns_box)
        self.card.append(self.scroller)

        self.empty = Gtk.Label(vexpand=True, visible=False, wrap=True)
        self.empty.add_css_class("nk-empty")
        self.card.append(self.empty)

        # Footer
        footer = Gtk.Box(spacing=12)
        footer.add_css_class("nk-footer")
        footer.append(Gtk.Label(label="Esc  close    ·    ↑ ↓  PgUp PgDn  scroll    ·    type to filter",
                                xalign=0, hexpand=True))
        footer.append(Gtk.Label(label=" · ".join(shorten_home(f) for f in keymap.files[:1])
                                or shorten_home(config_path), xalign=1))
        self.card.append(footer)

        if keymap.error:
            self.search.set_sensitive(False)
            self.scroller.set_visible(False)
            self.empty.set_visible(True)
            self.empty.remove_css_class("nk-empty")
            self.empty.add_css_class("nk-error")
            self.empty.set_label(f"Could not read the niri config:\n\n{keymap.error}")
            self.count.set_label("")
        else:
            for name, binds in group_binds(keymap.binds):
                self._add_section(name, binds)
            self._apply_filter()

        keys = Gtk.EventControllerKey()
        keys.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        keys.connect("key-pressed", self._on_key)
        self.win.add_controller(keys)

        click = Gtk.GestureClick()
        click.connect("pressed", self._on_click)
        self.backdrop.add_controller(click)

        self.win.present()
        self.search.grab_focus()

    def close(self) -> None:
        self.win.close()

    def _add_section(self, name: str, binds: list[Bind]) -> None:
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        head = Gtk.Box(spacing=8)
        head.add_css_class("nk-section-head")
        title = Gtk.Label(label=name.upper(), xalign=0, hexpand=True, wrap=True)
        title.add_css_class("nk-section-title")
        count = Gtk.Label(label=str(len(binds)))
        count.add_css_class("nk-section-count")
        head.append(title)
        head.append(count)
        box.append(head)
        rows = []
        for b in binds:
            row, weight = self._make_row(b)
            box.append(row)
            rows.append((row, b.haystack, weight))
        self.sections.append(Section(box, count, rows))

    def _make_row(self, b: Bind):
        row = Gtk.Box(spacing=14)
        row.add_css_class("nk-row")
        row.set_tooltip_text(f"{b.combo}\n{b.action}\n{shorten_home(b.file)}:{b.line}")

        text = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1,
                       hexpand=True, valign=Gtk.Align.CENTER)
        title = Gtk.Label(label=b.title, xalign=0, wrap=True,
                          wrap_mode=Pango.WrapMode.WORD_CHAR)
        text.append(title)
        weight = 1.0

        details = []
        if b.custom_title:
            details.append(f"<tt>{GLib.markup_escape_text(b.action)}</tt>")
        details += [GLib.markup_escape_text(f) for f in b.flags]
        if b.note:
            details.append(f"<i>{GLib.markup_escape_text(b.note)}</i>")
        if details:
            detail = Gtk.Label(xalign=0, wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR)
            detail.set_markup("  ·  ".join(details))
            detail.add_css_class("nk-bind-detail")
            text.append(detail)
            weight += 0.6

        keys = Gtk.Box(spacing=4, valign=Gtk.Align.CENTER, halign=Gtk.Align.END)
        parts = [(m, True) for m in b.mods] + [(b.key, False)]
        for i, (label, is_mod) in enumerate(parts):
            if i:
                plus = Gtk.Label(label="+")
                plus.add_css_class("nk-plus")
                keys.append(plus)
            cap = Gtk.Label(label=label)
            cap.add_css_class("nk-key")
            if is_mod:
                cap.add_css_class("nk-mod")
            keys.append(cap)

        row.append(text)
        row.append(keys)
        return row, weight

    def _apply_filter(self, *_args) -> None:
        query = self.search.get_text().strip()
        terms = query.lower().split()
        shown = 0
        for sec in self.sections:
            sec.visible_rows, sec.visible_weight = 0, 0.0
            for row, haystack, weight in sec.rows:
                match = all(t in haystack for t in terms)
                row.set_visible(match)
                if match:
                    sec.visible_rows += 1
                    sec.visible_weight += weight
            sec.count_label.set_label(str(sec.visible_rows))
            shown += sec.visible_rows
        self.count.set_label(f"{self.total} bindings" if not terms
                             else f"{shown} of {self.total} bindings")
        self._layout_columns()
        self.scroller.set_visible(shown > 0)
        self.empty.set_visible(shown == 0)
        if shown == 0:
            self.empty.set_label(f"No keybindings match “{query}”" if query
                                 else "No keybindings found in the niri config")
        self.scroller.get_vadjustment().set_value(0)

    def _layout_columns(self) -> None:
        for col in self.columns:
            child = col.get_first_child()
            while child is not None:
                nxt = child.get_next_sibling()
                col.remove(child)
                child = nxt
        visible = [s for s in self.sections if s.visible_rows]
        runs = linear_partition([2.0 + s.visible_weight for s in visible], len(self.columns))
        for col, run in zip(self.columns, runs):
            for i in run:
                col.append(visible[i].box)

    def _on_key(self, _ctrl, keyval, _keycode, state) -> bool:
        ctrl = bool(state & Gdk.ModifierType.CONTROL_MASK)
        if keyval == Gdk.KEY_Escape or (ctrl and keyval in (Gdk.KEY_q, Gdk.KEY_w)):
            self.close()
            return True
        adj = self.scroller.get_vadjustment()
        page = adj.get_page_size() * 0.85
        delta = {Gdk.KEY_Down: 60, Gdk.KEY_Up: -60,
                 Gdk.KEY_Page_Down: page, Gdk.KEY_Page_Up: -page}.get(keyval)
        if delta is None:
            return False
        adj.set_value(adj.get_value() + delta)
        return True

    def _on_click(self, _gesture, _n_press, x, y) -> None:
        picked = self.backdrop.pick(x, y, Gtk.PickFlags.DEFAULT)
        if picked is None or not (picked is self.card or picked.is_ancestor(self.card)):
            self.close()


def run_gui(config_path: str) -> int:
    load_gtk()
    app = Gtk.Application(application_id=APP_ID)
    overlay: Overlay | None = None

    def on_activate(app) -> None:
        nonlocal overlay
        # A second launch activates the running instance, which toggles it closed.
        if overlay is not None:
            overlay.close()
            return
        keymap = load_keymap(config_path)
        for w in keymap.warnings:
            print(f"niri-keybinds: {w}", file=sys.stderr)
        overlay = Overlay(app, keymap, config_path)

    app.connect("activate", on_activate)
    return app.run([sys.argv[0]])


# ──────────────────────────────── CLI ────────────────────────────────

def print_list(keymap: Keymap) -> int:
    for w in keymap.warnings:
        print(f"warning: {w}", file=sys.stderr)
    if keymap.error:
        print(f"error: {keymap.error}", file=sys.stderr)
        return 1
    tty = sys.stdout.isatty()
    bold, dim, reset = ("\033[1m", "\033[2m", "\033[0m") if tty else ("", "", "")
    width = min(34, max((len(b.keys_text) for b in keymap.binds), default=0))
    for i, (section, binds) in enumerate(group_binds(keymap.binds)):
        print(("\n" if i else "") + f"{bold}{section}{reset}")
        for b in binds:
            line = f"  {b.keys_text:<{width}}  {b.title}"
            extra = ([b.action] if b.custom_title else []) + b.flags + ([b.note] if b.note else [])
            if extra:
                line += f"  {dim}[{' · '.join(extra)}]{reset}"
            print(line)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Show niri key bindings.")
    ap.add_argument("--config", "-c", default=None,
                    help="config file to read (default: $NIRI_CONFIG or ~/.config/niri/config.kdl)")
    ap.add_argument("--list", "-l", action="store_true", help="print bindings to stdout and exit")
    args = ap.parse_args()
    config_path = os.path.expanduser(args.config) if args.config else default_config_path()
    if args.list:
        return print_list(load_keymap(config_path))
    return run_gui(config_path)


if __name__ == "__main__":
    sys.exit(main())
