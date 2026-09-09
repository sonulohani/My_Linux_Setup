-- HyprGlass liquid-glass effects
-- hyprpm loads the plugin; the guard keeps startup safe if it is unavailable.
if hl.plugin.hyprglass then
	local hg = hl.plugin.hyprglass

	hg.config({
		enabled = true,
		manage_window_blur = true,
		default_theme = "dark",
		default_preset = "glass",
		layers = {
			enabled = true,
			live_resample = true,
			live_resample_fps = 30,
		},
	})

	-- Noctalia shell surfaces currently used by this setup.
	hg.layer("noctalia-bar-default", {
		preset = "glass",
		mask_threshold = 0.05,
	})
	hg.layer("noctalia-dock", {
		preset = "glass",
		mask_threshold = 0.05,
	})
	hg.layer("noctalia-notification", {
		preset = "glass",
		mask_threshold = 0.05,
	})
	hg.layer("noctalia-panel", {
		preset = "glass",
		mask_threshold = 0.05,
	})
	hg.layer("noctalia-attached-panel", {
		preset = "glass",
		mask_threshold = 0.05,
	})
	hg.layer("noctalia-osd", {
		preset = "glass",
		mask_threshold = 0.05,
	})
	hg.layer("noctalia-window-switcher", {
		preset = "glass",
		mask_threshold = 0.05,
	})

	-- Presets
	hg.preset("clear", {
		glass_opacity = 0.8,
		blur_strength = 1.5,
		dark = { brightness = 0.7 },
		light = { brightness = 1.2 },
	})

	hg.preset("contrasted", {
		inherits = "high_contrast",
		contrast = 1.2,
		adaptive_dim = 1.5,
		dark = { tint_color = 0x02142aa9 },
	})
end
