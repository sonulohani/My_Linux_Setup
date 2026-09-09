-- Input configuration

hl.config({
	input = {
		-- sensitivity = -0.25,
		accel_profile = "flat",
		follow_mouse = 0,
		focus_on_close = 0,
	},
	-- Uncomment the section below to enable software cursors; this can help with cursor display or behavior issues
	-- cursor = {
	--     no_hardware_cursors = 1,
	-- },
})

-- Three fingers navigate the horizontal scrolling tape and workspaces.
hl.gesture({ fingers = 3, direction = "horizontal", action = "scroll_move" })
hl.gesture({
	fingers = 3,
	direction = "up",
	action = function()
		hl.exec_cmd("hyprctl dispatch workspace m-1")
	end,
})
hl.gesture({
	fingers = 3,
	direction = "down",
	action = function()
		hl.exec_cmd("hyprctl dispatch workspace m+1")
	end,
})

-- Noctalia's window switcher is its Hyprland overview equivalent.
hl.gesture({
	fingers = 4,
	direction = "up",
	action = function()
		hl.exec_cmd("noctalia msg window-switcher")
	end,
})
hl.gesture({
	fingers = 4,
	direction = "down",
	action = function()
		hl.exec_cmd("noctalia msg window-switcher close")
	end,
})
