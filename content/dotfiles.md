Title: dotfiles
Date: 2014-07-27 9:43AM
Category: code
Tags: dotfiles, git, tmux, vim, xmonad, zsh

My [dotfiles](https://github.com/nevillelyh/dotfiles/) is probably the most copied code among my coworkers and today I will give a little break down of the code base.

## zsh

I switched to [zsh](http://www.zsh.org/) 3 years ago and never looked back. There's also [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh), a framework for managing ZSH configuration. The features I found most useful are:

- Tab completion, including hostnames and arguments
- History across multiple sessions
- Plugins and themes

My [.zshrc](https://github.com/nevillelyh/dotfiles/blob/master/.zshrc) is mostly out of the box with some [aliases](https://github.com/nevillelyh/dotfiles/blob/master/.dotfiles/zsh/zshrc) and a few plugins thrown in but decided to create my own [theme](https://github.com/nevillelyh/dotfiles/blob/master/.dotfiles/zsh/sinisa.zsh-theme). I use colors for hostname in the prompt, green for local and red for remote. I also tweaked `git` status a bit to show untracked files (red dots), unstaged (yellow) & staged (green) changes, plus number stashed changes since that's the one thing I keep doing and forgetting about.

## git

I use `git` both for work and personal projects, plus contributing to open source projects on [GitHub](https://github.com/). My [.gitconfig](https://github.com/nevillelyh/dotfiles/blob/master/.gitconfig) includes both a global `gitignore` file and a `templatedir`, which includes hooks for [ctags](http://ctags.sourceforge.net/) and [Gerrit](https://code.google.com/p/gerrit/). The hooks are installed automatically for every repo.

Since I type hundreds of `git` commands on a daily basis, I aliased `git` to simply `g` and added a bunch more for `checkout`, `commit`, `diff`, `rebase`, etc. I also added several log aliases with better formats, including one-liner color history, graph, and commits only by me.

I also have a few `git-*` [scripts](https://github.com/nevillelyh/dotfiles/tree/master/.dotfiles/scripts) to make my workflow a bit easier.

## vim

I've been a `vim` user for 15+ years and have come up with a pretty good set of settings and plugins. I keep most complex settings in a [vimrc.d](https://github.com/nevillelyh/dotfiles/tree/master/.vim/vimrc.d) directory and load them from [.vimrc](https://github.com/nevillelyh/dotfiles/blob/master/.vimrc), which is kept short with mostly look and feel plus some basic settings. This way I can easily copy just the `.vimrc` to a remote server and have some decent setting to work with.

I depend on [many plugins](https://github.com/nevillelyh/dotfiles/blob/master/.vim/vimrc.d/vundle.vim) to get things done, roughly in the following categories.

- [vim-powerline](https://github.com/Lokaltog/vim-powerline) and [vim-colors-solarized](https://github.com/altercation/vim-colors-solarized) for look and feel. You might need to patch fonts for the fancy symbols though.
- [gitv](https://github.com/gregsexton/gitv), [vim-fugitive](https://github.com/tpope/vim-fugitive) and [vim-git](https://github.com/tpope/vim-git) for `git` integration.
- [tagbar](https://github.com/majutsushi/tagbar) and [nerdtree](https://github.com/scrooloose/nerdtree) for sidebar, which I mapped to `alt-1` and `alt-2`
- [syntastic](https://github.com/scrooloose/syntastic), probably the most valuable one, integrates with [flake8](https://flake8.readthedocs.org/) and other tools for syntax checking.
- A few more for shortcuts like quotes, tab completion, and commenting.
- And a few more for syntax highlighting of various programming languages that I work with.

## tmux

As a data and backend engineer, I spend most of my time on remote servers and rely heavily on [tmux](http://tmux.sourceforge.net/) for session management. I tend to create one session for each project and split windows when necessary for coding, tailing logs and interacting with the build system.

I changed my prefix from `ctrl-b` to &#96; since that's the least used key and not too hard to reach.I also added bindings to split a window horizontally and vertically, plus `vim` style `hjkl` keys to move around. I also use [tmux-powerline](https://github.com/erikw/tmux-powerline) for a nicer status line. The same `vim-powerline` fonts work here too.

One thing I noticed is that re-attached `screen` or `tmux` doesn't work well with SSH forwarding since the `SSH_AUTH_SOCK` is different for each session. So I created a [snippet](https://github.com/nevillelyh/dotfiles/blob/master/.dotfiles/zsh/zshrc#L55) to `symlink` sock files to the same location.

## xmonad

I use a Linux desktop at work and use [xmonad](http://xmonad.org/) as my window manager. It's a tiling window manager which means instead of move and resize windows yourself, the manager tiles windows for you based on predefined layouts. Once I figured out a workflow, I found myself a lot more productive even when multi-tasking.

The main layout in my [xmonad.hs](https://github.com/nevillelyh/dotfiles/blob/master/.xmonad/xmonad.hs) uses left 3/5 of the screen for main window and the right 2/5 for others. The second layout splits horizontally 50/50 while the third is a grid layout, perfect for [Cluster SSH](http://sourceforge.net/projects/clusterssh/) into many servers.

There are also a couple of key bindings, including ones to control [Spotify](https://www.spotify.com/) via this [shell script](https://github.com/nevillelyh/dotfiles/blob/master/.dotfiles/scripts/spotify.sh).

## bootstrapping

I started with putting my `HOME` directory in a `git` repo a few years ago, and over time added various dependencies across different platforms, e.g. [aptitude](http://aptitude.alioth.debian.org/doc/en/), [homebrew](http://brew.sh/), [pip](http://pip.readthedocs.org/) and [Vundle](https://github.com/gmarik/Vundle.vim). Furthermore I access to a lot of virtual and bare-metal hosts and would like to streamline the processing of getting set up on a new host.

Inspired by `homebrew`, I created a [bootstrap-dotfiles.sh](https://github.com/nevillelyh/dotfiles/blob/master/.dotfiles/scripts/bootstrap-dotfiles.sh) that automates everything for me. The script is cross-platform and uses `aptitude` on Debian or Ubuntu and `brew` on Mac OS X for native packages. It also installs Python packages via `pip`, vim plugins via Vundle, checks out the git repo into `HOME` and changes the default shell to `zsh`.

## summary

With this setup I can easily move into a new environment with all the tools and shortcuts configured exactly the same way. Nevertheless I still try to tweak it constantly, removing stuff I rarely use and adding new ones for things I found myself doing repeatedly. And that's the same advice I gave to people who borrow my dotfiles, add one thing at a time and tweak it to your liking. Hope you all figure out something that makes you most productive.
