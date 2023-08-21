-- Pull in the wezterm API
local wezterm = require 'wezterm'

-- This table will hold the configuration.
local config = {}

-- In newer versions of wezterm, use the config_builder which will
-- help provide clearer error messages
if wezterm.config_builder then
  config = wezterm.config_builder()
end

-- This is where you actually apply your config choices

-- For example, changing the color scheme:
config.color_scheme = 'Catppuccin Mocha'
config.enable_scroll_bar = true
config.font = wezterm.font('Monolisa Nerd Font')
config.font_size = 11.0
config.window_decorations = "RESIZE"
config.window_background_opacity = 0.95
config.use_fancy_tab_bar = false

-- and finally, return the configuration to wezterm
return config

