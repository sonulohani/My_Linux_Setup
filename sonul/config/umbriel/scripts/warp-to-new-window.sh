#!/bin/sh
# Warp the cursor onto newly opened tiled windows that take keyboard focus.
# With input.focus.follows_mouse, a pointer left over a maximized window would
# otherwise pull focus back to it and scroll the new window out of view.
# Floating windows (dialogs, picture-in-picture) always open on top, so they
# are left alone.

exec 9>"${XDG_RUNTIME_DIR:-/tmp}/umbriel-warp-to-new-window.lock"
flock -n 9 || exit 0

umbriel subscribe windows |
  jq --unbuffered -rn '
    foreach (inputs | select(.event == "windows") | .data) as $wins (
      {seen: null, warp: []};
      .seen as $seen
      | .warp = (if $seen == null then [] else
          [$wins[] | select(($seen[.id] | not) and .active and (.floating | not)) | .id]
        end)
      | .seen = ($wins | map({key: .id, value: true}) | from_entries);
      .warp[]
    )' |
  while IFS= read -r id; do
    umbriel msg "window-focus-warp:$id"
  done
