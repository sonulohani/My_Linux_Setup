-- Optional per-user keybind overrides (managed by DMS). Loaded after default binds.
--
hl.bind("SUPER + Return", hl.dsp.exec_cmd("kitty"))
hl.bind("SUPER + E", hl.dsp.exec_cmd("nautilus"))
hl.bind("SUPER + CTRL + W", hl.dsp.exec_cmd("dms ipc wallpaperCarousel toggle"))
hl.bind("SUPER + CTRL + P", hl.dsp.exec_cmd("dms ipc call quickCapture screenshot region edit"))
