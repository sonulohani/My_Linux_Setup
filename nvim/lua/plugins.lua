local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", -- latest stable release
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

local plugins = {
  {
    "nvim-tree/nvim-tree.lua",
    version = "*",
    lazy = false,
    dependencies = {
      "nvim-tree/nvim-web-devicons",
    }
  },
  "williamboman/mason.nvim",
  "williamboman/mason-lspconfig.nvim",
  "neovim/nvim-lspconfig",
  "mfussenegger/nvim-dap",
  "rcarriga/nvim-dap-ui",
  "mfussenegger/nvim-lint",
  "mhartington/formatter.nvim",
  {
    'nvim-telescope/telescope.nvim', tag = '0.1.2',
-- or                              , branch = '0.1.x',
      dependencies = { 'nvim-lua/plenary.nvim' }
  },
  "nvim-treesitter/nvim-treesitter",
  "marko-cerovac/material.nvim",
  {
    "nvim-lualine/lualine.nvim",
    dependencies = { 'nvim-tree/nvim-web-devicons', opt = true }
  },
  "tanvirtin/monokai.nvim",
  {
    'goolord/alpha-nvim',
    event = "VimEnter",
    dependencies = { 'nvim-tree/nvim-web-devicons' },
  },
  'hrsh7th/cmp-nvim-lsp',
  'hrsh7th/cmp-buffer',
  'hrsh7th/cmp-path',
  'hrsh7th/cmp-cmdline',
  'hrsh7th/nvim-cmp',
  'hrsh7th/cmp-vsnip',
  'hrsh7th/vim-vsnip',
  'L3MON4D3/LuaSnip',
  'saadparwaiz1/cmp_luasnip',
  'SirVer/ultisnips',
  'quangnguyen30192/cmp-nvim-ultisnips',
  'dcampos/nvim-snippy',
  'dcampos/cmp-snippy',
}
local opts = {
}

require("lazy").setup(plugins, opts)

----------------------------- EXTRA CONFIG ----------------------------
-- Color scheme
require('monokai').setup {}

-- lualine
require('plugins/lualine_setup')
require('plugins/alpha_nvim_setup')
require('plugins/lsp_config_setup')
require('plugins/nvim_cmp_setup')
