-- Input configuration

hl.config({
	input = {
		-- sensitivity = -0.25,
		accel_profile = "flat"
	},
	-- Uncomment the section below to enable software cursors; this can help with cursor display or behavior issues
	-- cursor = {
	--     no_hardware_cursors = 1,
	-- },
})

-- Three fingers scroll windows horizontally within the current workspace.
hl.gesture({ fingers = 3, direction = "horizontal", action = "scroll_move" })

-- Four fingers swipe horizontally to switch workspaces.
hl.gesture({ fingers = 4, direction = "horizontal", action = "workspace" })

-- Four fingers up/down open/close the hymission overview.
hl.gesture({
	fingers = 4,
	direction = "up",
	action = function()
		hl.plugin.hymission.open()
	end,
})
hl.gesture({
	fingers = 4,
	direction = "down",
	action = function()
		hl.plugin.hymission.close()
	end,
})
