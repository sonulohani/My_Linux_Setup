#!/usr/bin/env python3
"""Niri-style keybind overlay for keybinds.kdl."""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import gi

gi.require_version("GtkLayerShell", "0.1")
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gio, Gdk, GLib, Gtk, GtkLayerShell  # noqa: E402

CFG_DIR = Path(__file__).resolve().parent
KEYBINDS_FILE = Path(os.environ.get("KEYBINDS_FILE", str(CFG_DIR / "keybinds.kdl")))
INPUT_FILE = CFG_DIR / "input.kdl"
MOD_KEY = "Super"

FIELD_SEP = "\x1f"
SECTION_RE = re.compile(r"^[ \t]*//[ \t]*─")
TITLE_RE = re.compile(r'hotkey-overlay-title="([^"]*)"')
PROP_RE = re.compile(
    r'[ \t]+(?:hotkey-overlay-title|allow-when-locked|allow-inhibiting|cooldown-ms|repeat)=("[^"]*"|[^ \t]+)'
)
SPAWN_SH_RE = re.compile(r'^spawn-sh[ \t]+"([^"]*)"')
SPAWN_RE = re.compile(r'^spawn[ \t]+"([^"]*)"')

ACTION_LABELS = {
    "show-hotkey-overlay": "Show Important Hotkeys",
    "close-window": "Close Focused Window",
    "focus-column-left": "Focus Column to the Left",
    "focus-column-right": "Focus Column to the Right",
    "move-column-left": "Move Column Left",
    "move-column-right": "Move Column Right",
    "focus-window-up": "Focus Window Up",
    "focus-window-down": "Focus Window Down",
    "move-window-up": "Move Window Up",
    "move-window-down": "Move Window Down",
    "focus-column-first": "Focus First Column",
    "focus-column-last": "Focus Last Column",
    "move-column-to-first": "Move Column to First",
    "move-column-to-last": "Move Column to Last",
    "focus-monitor-left": "Focus Monitor Left",
    "focus-monitor-right": "Focus Monitor Right",
    "focus-monitor-up": "Focus Monitor Up",
    "focus-monitor-down": "Focus Monitor Down",
    "move-column-to-monitor-left": "Move Column to Monitor Left",
    "move-column-to-monitor-right": "Move Column to Monitor Right",
    "move-column-to-monitor-up": "Move Column to Monitor Up",
    "move-column-to-monitor-down": "Move Column to Monitor Down",
    "focus-workspace-down": "Switch Workspace Down",
    "focus-workspace-up": "Switch Workspace Up",
    "focus-workspace-previous": "Switch to Previous Workspace",
    "move-column-to-workspace-down": "Move Column to Workspace Down",
    "move-column-to-workspace-up": "Move Column to Workspace Up",
    "expand-column-to-available-width": "Expand Column to Available Width",
    "center-column": "Center Column",
    "center-visible-columns": "Center Visible Columns",
    "toggle-window-floating": "Move Window Between Floating and Tiling",
    "fullscreen-window": "Fullscreen Window",
    "toggle-column-tabbed-display": "Toggle Column Tabbed Display",
    "screenshot": "Take a Screenshot",
    "screenshot-screen": "Take a Screenshot of Screen",
    "screenshot-window": "Take a Screenshot of Window",
    "toggle-keyboard-shortcuts-inhibit": "Toggle Keyboard Shortcuts Inhibit",
    "quit": "Exit niri",
    "power-off-monitors": "Power Off Monitors",
    "toggle-overview": "Open the Overview",
}

SPECIAL_KEYS = {
    "XF86AudioRaiseVolume": "Volume Up",
    "XF86AudioLowerVolume": "Volume Down",
    "XF86AudioMute": "Mute Output",
    "XF86AudioMicMute": "Mute Microphone",
    "XF86AudioNext": "Media Next",
    "XF86AudioPrev": "Media Previous",
    "XF86AudioPlay": "Media Play/Pause",
    "XF86AudioPause": "Media Play/Pause",
    "XF86MonBrightnessUp": "Brightness Up",
    "XF86MonBrightnessDown": "Brightness Down",
}

KEY_PART_LABELS = {
    "Mod": lambda: MOD_KEY,
    "CTRL": "Ctrl",
    "ALT": "Alt",
    "Shift": "Shift",
    "Return": "Enter",
    "Equal": "=",
    "Minus": "-",
    "Escape": "Esc",
    "ESCAPE": "Esc",
    "WheelScrollDown": "Wheel Scroll Down",
    "WheelScrollUp": "Wheel Scroll Up",
    "WheelScrollLeft": "Wheel Scroll Left",
    "WheelScrollRight": "Wheel Scroll Right",
    "Prior": "Page Up",
    "Next": "Page Down",
    "Print": "PrtSc",
    "TAB": "Tab",
}

CSS = b"""
window {
    background-color: transparent;
}

.overlay-border {
    background-color: #1a1a1a;
    border: 4px solid rgb(128, 204, 255);
    padding: 24px 28px 20px 36px;
}

.overlay-title {
    color: #ffffff;
    font-family: sans-serif;
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 12px;
}

.section-title {
    color: rgb(140, 210, 255);
    font-family: sans-serif;
    font-size: 12px;
    font-weight: bold;
    margin-top: 14px;
    margin-bottom: 6px;
}

.section-title:first-child {
    margin-top: 0;
}

.section-rule {
    background-color: rgba(128, 204, 255, 0.25);
    min-height: 1px;
    margin-bottom: 8px;
}

.keybind-row {
    margin-bottom: 6px;
}

.key-badge {
    background-color: #2e2e2e;
    color: #ffffff;
    font-family: monospace;
    font-size: 13px;
    padding: 4px 12px;
    margin-right: 24px;
}

.action-label {
    color: #f2f2f2;
    font-family: sans-serif;
    font-size: 14px;
}

.scrolled {
    background-color: transparent;
}

.scrolled scrollbar.vertical {
    background-color: transparent;
}

.scrolled scrollbar slider {
    background-color: rgba(128, 204, 255, 0.35);
    border-radius: 4px;
}

.hint-label {
    color: rgba(255, 255, 255, 0.45);
    font-family: sans-serif;
    font-size: 11px;
    margin-top: 10px;
}
"""


@dataclass
class Keybind:
    key: str
    description: str


@dataclass
class Section:
    name: str
    binds: list[Keybind] = field(default_factory=list)


def read_mod_key() -> None:
    global MOD_KEY
    if not INPUT_FILE.is_file():
        return
    match = re.search(r'mod-key[ \t]+"([^"]+)"', INPUT_FILE.read_text())
    if match and match.group(1) in {"Super", "Alt", "Shift", "Ctrl", "Mod5", "Mod3"}:
        MOD_KEY = match.group(1)


def prettify_key_part(part: str) -> str:
    part = part.strip()
    if not part:
        return ""
    if part in KEY_PART_LABELS:
        value = KEY_PART_LABELS[part]
        return value() if callable(value) else value
    if len(part) == 1 and part.isalnum():
        return part.upper()
    return part


def format_key_combo(combo: str) -> str:
    parts = [prettify_key_part(p) for p in combo.split("+") if p.strip()]
    return " + ".join(parts)


def describe_spawn_sh(command: str) -> str:
    patterns = {
        "plugin:clipper toggle": "Toggle Clipboard History",
        "volume increase": "Volume Up",
        "volume decrease": "Volume Down",
        "volume muteOutput": "Mute Output",
        "volume muteInput": "Mute Microphone",
        "media next": "Media Next",
        "media previous": "Media Previous",
        "media playPause": "Media Play/Pause",
        "brightness increase": "Brightness Up",
        "brightness decrease": "Brightness Down",
    }
    for needle, label in patterns.items():
        if needle in command:
            return label
    return f"Spawn {command.split()[0] if command.split() else command}"


def describe_action(action: str, combo: str) -> str:
    if combo in SPECIAL_KEYS:
        return SPECIAL_KEYS[combo]

    if action in ACTION_LABELS:
        return ACTION_LABELS[action]

    if action.startswith("focus-workspace "):
        return f"Switch to Workspace {action.split(' ', 1)[1]}"
    if action.startswith("move-column-to-workspace "):
        return f"Move Column to Workspace {action.split(' ', 1)[1]}"
    if action.startswith("set-column-width "):
        return f"Set Column Width {action.split(' ', 1)[1]}"
    if action.startswith("set-window-height "):
        return f"Set Window Height {action.split(' ', 1)[1]}"
    if action.startswith("spawn-sh "):
        return describe_spawn_sh(action.split(" ", 1)[1])
    if action.startswith("spawn "):
        return f"Spawn {action.split(' ', 1)[1]}"

    return action


def extract_section(line: str) -> str | None:
    if not SECTION_RE.match(line):
        return None
    text = re.sub(r"^[^/]*//[ \t]*─+[ \t]*", "", line)
    text = re.sub(r"[ \t]*─+.*$", "", text).strip()
    return text or "General"


def strip_inline_comment(line: str) -> str:
    return re.sub(r"[ \t]+//.*$", "", line).strip()


def strip_properties(text: str) -> str:
    while True:
        match = PROP_RE.search(text)
        if not match:
            break
        text = text[: match.start()] + text[match.end() :]
    return text.strip()


def extract_action(block: str) -> str:
    inner = block.strip()
    inner = re.sub(r"^\{[ \t]*", "", inner)
    inner = re.sub(r";[ \t]*\}[ \t]*$", "", inner)
    inner = re.sub(r";[ \t]*$", "", inner).strip()

    match = SPAWN_SH_RE.match(inner)
    if match:
        return f"spawn-sh {match.group(1)}"
    match = SPAWN_RE.match(inner)
    if match:
        return f"spawn {match.group(1)}"
    return inner


def parse_keybinds(path: Path) -> list[Section]:
    if not path.is_file():
        raise FileNotFoundError(f"keybinds file not found: {path}")

    sections: list[Section] = []
    current = Section(name="General")

    for raw_line in path.read_text().splitlines():
        line = raw_line.rstrip("\n")
        section_name = extract_section(line)
        if section_name is not None:
            if current.binds:
                sections.append(current)
            current = Section(name=section_name)
            continue

        if line.strip().startswith("//"):
            continue
        if re.match(r"^[ \t]*binds[ \t]*\{", line):
            continue
        if re.match(r"^[ \t]*\}[ \t]*$", line):
            continue
        if "{" not in line:
            continue

        line = strip_inline_comment(line)
        if re.match(r"^binds[ \t]*\{", line):
            continue

        brace = line.index("{")
        before = line[:brace]
        block = line[brace:]

        title_match = TITLE_RE.search(before)
        title = title_match.group(1) if title_match else ""
        combo = strip_properties(before)
        action = extract_action(block)

        if not combo or not action or combo == "binds":
            continue

        key = format_key_combo(combo)
        description = title if title else describe_action(action, combo)
        current.binds.append(Keybind(key=key, description=description))

    if current.binds:
        sections.append(current)

    return sections


class KeybindsOverlay(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(application_id="dev.niri.keybinds-overlay")
        self.window: Gtk.Window | None = None
        self.content_box: Gtk.Box | None = None
        self.file_monitor: Gio.FileMonitor | None = None
        self.reload_source_id: int | None = None
        self.sections: list[Section] = []

    def do_startup(self) -> None:
        Gtk.Application.do_startup(self)
        self.hold()

    def do_activate(self) -> None:
        try:
            if self.window is None:
                self.window = self._build_window()
                self._setup_file_monitor()
            self._show()
        except Exception as exc:
            print(f"keybinds-overlay error: {exc}", file=sys.stderr)
            raise

    def _setup_file_monitor(self) -> None:
        if not KEYBINDS_FILE.is_file():
            return

        gfile = Gio.File.new_for_path(str(KEYBINDS_FILE))
        self.file_monitor = gfile.monitor_file(Gio.FileMonitorFlags.NONE, None)
        self.file_monitor.connect("changed", self._on_keybinds_file_changed)

        if INPUT_FILE.is_file():
            input_file = Gio.File.new_for_path(str(INPUT_FILE))
            input_monitor = input_file.monitor_file(Gio.FileMonitorFlags.NONE, None)
            input_monitor.connect("changed", self._on_keybinds_file_changed)

    def _on_keybinds_file_changed(self, *_args) -> None:
        if self.reload_source_id is not None:
            GLib.source_remove(self.reload_source_id)
        self.reload_source_id = GLib.timeout_add(250, self._reload_from_file)

    def _reload_from_file(self) -> bool:
        self.reload_source_id = None
        try:
            self._reload_content()
        except Exception as exc:
            print(f"keybinds-overlay reload error: {exc}", file=sys.stderr)
        return False

    def _reload_content(self) -> None:
        if self.content_box is None:
            return

        read_mod_key()
        self.sections = parse_keybinds(KEYBINDS_FILE)

        for child in self.content_box.get_children():
            self.content_box.remove(child)

        self._populate_content(self.content_box, self.sections)
        self.content_box.show_all()

    def _show(self) -> None:
        if self.window is None:
            return

        try:
            self._reload_content()
        except Exception as exc:
            print(f"keybinds-overlay reload error: {exc}", file=sys.stderr)

        GtkLayerShell.set_keyboard_interactivity(self.window, True)
        self.window.show()
        self.window.show_all()
        self.window.present()
        self.window.set_keep_above(True)

    def _hide(self) -> None:
        if self.window is None or not self.window.get_visible():
            return
        GtkLayerShell.set_keyboard_interactivity(self.window, False)
        self.window.hide()

    def _populate_content(self, content: Gtk.Box, sections: list[Section]) -> None:
        max_key_width = max(
            (len(bind.key) for section in sections for bind in section.binds),
            default=10,
        )
        key_col_width = max(max_key_width * 9 + 32, 320)

        for section in sections:
            section_label = Gtk.Label(label=section.name, xalign=0)
            section_label.set_margin_start(4)
            section_label.get_style_context().add_class("section-title")
            content.pack_start(section_label, False, False, 0)

            rule = Gtk.Box()
            rule.get_style_context().add_class("section-rule")
            rule.set_size_request(-1, 1)
            rule.set_margin_start(4)
            rule.set_margin_end(4)
            content.pack_start(rule, False, False, 0)

            for bind in section.binds:
                row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
                row.set_margin_start(4)
                row.get_style_context().add_class("keybind-row")

                key_label = Gtk.Label(label=bind.key)
                key_label.set_xalign(0)
                key_label.set_halign(Gtk.Align.START)
                key_label.set_valign(Gtk.Align.START)
                key_label.set_size_request(key_col_width, -1)
                key_label.get_style_context().add_class("key-badge")
                row.pack_start(key_label, False, False, 0)

                if "<" in bind.description and ">" in bind.description:
                    action_label = Gtk.Label()
                    action_label.set_markup(bind.description)
                else:
                    action_label = Gtk.Label(label=bind.description)
                action_label.set_xalign(0)
                action_label.set_halign(Gtk.Align.START)
                action_label.set_valign(Gtk.Align.START)
                action_label.set_line_wrap(True)
                action_label.set_max_width_chars(72)
                action_label.get_style_context().add_class("action-label")
                row.pack_start(action_label, True, True, 0)

                content.pack_start(row, False, False, 0)

    def _build_window(self) -> Gtk.Window:
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        window.set_title("Important Hotkeys")
        window.set_decorated(False)
        window.set_resizable(False)
        window.set_default_size(1020, 760)
        window.set_keep_above(True)
        window.set_skip_taskbar_hint(True)
        window.set_skip_pager_hint(True)
        window.set_type_hint(Gdk.WindowTypeHint.NOTIFICATION)

        GtkLayerShell.init_for_window(window)
        GtkLayerShell.set_layer(window, GtkLayerShell.Layer.OVERLAY)
        GtkLayerShell.set_keyboard_mode(window, GtkLayerShell.KeyboardMode.ON_DEMAND)
        GtkLayerShell.set_exclusive_zone(window, -1)

        frame = Gtk.EventBox()
        frame.set_size_request(980, -1)
        window.add(frame)

        border_frame = Gtk.Frame()
        border_frame.set_shadow_type(Gtk.ShadowType.NONE)
        border_frame.get_style_context().add_class("overlay-border")
        frame.add(border_frame)

        body = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        border_frame.add(body)

        title = Gtk.Label(label="Important Hotkeys")
        title.set_halign(Gtk.Align.CENTER)
        title.get_style_context().add_class("overlay-title")
        body.pack_start(title, False, False, 0)

        scroll_wrap = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        body.pack_start(scroll_wrap, True, True, 0)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_shadow_type(Gtk.ShadowType.NONE)
        scrolled.get_style_context().add_class("scrolled")
        screen = Gdk.Screen.get_default()
        monitor = screen.get_primary_monitor()
        geometry = screen.get_monitor_geometry(monitor)
        scrolled.set_max_content_height(int(geometry.height * 0.78))
        scrolled.set_min_content_height(640)
        scrolled.set_size_request(-1, 640)
        scroll_wrap.pack_start(scrolled, True, True, 0)

        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        scrolled.add(self.content_box)

        hint = Gtk.Label(label="Press Esc to close")
        hint.set_halign(Gtk.Align.CENTER)
        hint.get_style_context().add_class("hint-label")
        body.pack_start(hint, False, False, 0)

        def on_key(_widget, event) -> bool:
            if event.keyval == Gdk.KEY_Escape:
                self._hide()
                return True
            return False

        window.connect("key-press-event", on_key)
        window.connect("delete-event", lambda *_: self._hide() or True)

        return window


def main() -> int:
    app = KeybindsOverlay()
    app.run(sys.argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
