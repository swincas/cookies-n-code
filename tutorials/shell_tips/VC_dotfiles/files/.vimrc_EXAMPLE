"""""""""""""""""""""""
" File:   .vimrc
" Author: Adam Batten
" Year:   2018
"""""""""""""""""""""""

" Use pathogen plugin manager
execute pathogen#infect()

""""""""""""""""""""""
" GENERAL
""""""""""""""""""""""
" Don't be compatible with vi
set nocompatible

" Set how many lines for VIM to remember
set history=500

"""""""""""""""""""""""
" COLOURS
"""""""""""""""""""""""
syntax enable                      " Enable syntax highlighting
colorscheme monokai                " Use monokai colourscheme

""""""""""""""""""""""
" USER INTERFACE
""""""""""""""""""""""

" TAB Settings
set expandtab                      " Tabs ARE spaces
set tabstop=4                      " Display the tabs as this many spaces
set softtabstop=4                  " The number of spaces a TAB is when editing
set shiftwidth=4
set autoindent
set smartindent

" Display Settings
set ruler                          " Always show position
set showcmd                        " Show incomplete commands
set number                         " Line numbers
set colorcolumn=80

" Make things easier
set backspace=indent,eol,start     " Backspace works like you would expect
set mouse=a                        " Enable mouse

" Disable Sound Errors
set vb
set noerrorbells
set novisualbell
set t_vb=
set tm=500

" Use for lightline package (pretty status bar)
set laststatus=2                   " Show the status bar
let g:lightline = {'colorscheme': 'wombat'} " Choose the colourscheme

" Use , for custom commands
let mapleader = ","

" Useful mappings for managing tabs
map <leader>tn :tabnew<cr>
map <leader>to :tabonly<cr>
map <leader>tc :tabclose<cr>
map <leader>tm :tabmove
map <leader>t<leader> :tabnext

" Spell check
map <leader>sc :setlocal spell<cr>

set spelllang=en
set spellfile=~/dotfiles/vim/spell/en.utf-8.add

" Return to last edit position when opening files (You want this!)
au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
