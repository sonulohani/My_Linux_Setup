-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
--
local keymap = vim.keymap.set

keymap("n", "<leader>d", '"_d', { noremap = true, silent = true })
keymap("x", "<leader>d", '"_d', { noremap = true, silent = true })
keymap("x", "<leader>p", '"_dP', { noremap = true, silent = true })

keymap("n", "<A-S-Up>", ":m .-2<CR>==", { desc = "Move line up" })
keymap("n", "<A-S-Down>", ":m .+1<CR>==", { desc = "Move line down" })
