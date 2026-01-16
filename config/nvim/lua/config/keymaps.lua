-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
--
local keymap = vim.keymap.set

keymap("n", "<leader>d", '"_d', { noremap = true, silent = true })
keymap("x", "<leader>d", '"_d', { noremap = true, silent = true })
keymap("x", "<leader>p", '"_dP', { noremap = true, silent = true })

-- Normal Mode (Move single line)
keymap("n", "<A-Down>", ":m .+1<CR>==", { desc = "Move line down" })
keymap("n", "<A-Up>", ":m .-2<CR>==", { desc = "Move line up" })

-- Visual Mode (Move selected block)
-- 'v' mode covers both Visual and Visual-Line modes
keymap("v", "<A-Down>", ":m '>+1<CR>gv=gv", { desc = "Move selection down" })
keymap("v", "<A-Up>", ":m '<-2<CR>gv=gv", { desc = "Move selection up" })