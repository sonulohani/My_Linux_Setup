-- Auto-start config
-- if you dont use UWSM add your auto start programs here, otherwise use XDG autostart https://wiki.archlinux.org/title/XDG_Autostart

local function apply_cursor_theme()
	local theme = os.getenv("XCURSOR_THEME")
	local size = os.getenv("XCURSOR_SIZE") or "24"
	if theme then
		hl.exec_cmd("hyprctl setcursor " .. theme .. " " .. size)
	end
end

hl.on("hyprland.start", function()
	hl.exec_cmd("dbus-update-activation-environment --systemd --all")
	apply_cursor_theme()
	hl.exec_cmd("noctalia")
	hl.exec_cmd("xhost +SI:localuser:root")
	hl.exec_cmd("snappy-switcher --daemon")
end)
