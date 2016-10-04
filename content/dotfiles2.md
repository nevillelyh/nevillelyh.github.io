Title: dotfiles update
Date: 2014-08-21 10:14PM
Category: code
Tags: dotfiles, tmux, vim

I've been using my current [dotfiles]({filename}dotfiles.md) setup for a while and felt it's time to freshen up. I focused on updating the look and feel of Vim and tmux this round.

First I switched to [molokai](https://github.com/tomasr/molokai) color theme for Vim, [TextMate](http://macromates.com/) (monokai) and [IntelliJ IDEA](http://www.jetbrains.com/idea/) (using [this](https://github.com/y3sh/Intellij-Colors-Sublime-Monokai)). I guess I grew tired of the old trusted [solarized](http://ethanschoonover.com/solarized), plus with my new MacBook Pro 13" at highest resolution, it just doesn't feel sharp enough.

The [vim-powerline](https://github.com/Lokaltog/vim-powerline) plugin I was using is being deprecated and replaced by [powerline](https://github.com/Lokaltog/powerline), which supports vim, tmux, zsh, and many others. However it requires Python and I had trouble using it with some really old Vim versions at work. So instead I switched to a pure VimL plugin, [vim-airline](https://github.com/bling/vim-airline). Not surprisingly there's a companion plugin, [tmuxline](https://github.com/edkolev/tmuxline.vim) for tmux as well. Both have no extra dependencies which is a big plus for me since I use the same dotfiles on Mac, my Ubuntu Trusty destop at work, and many Debian Squeeze servers.

I also updated a couple of other Vim plugins along the process, replacing [vim-snipmate](https://github.com/garbas/vim-snipmate) with [ultisnips](https://github.com/SirVer/ultisnips), [vim-bad-whitespace](https://github.com/bitc/vim-bad-whitespace) with [vim-better-whitespace](https://github.com/ntpeters/vim-better-whitespace) (no pun intended), and adding [vim-gutter](https://github.com/airblade/vim-gitgutter). The biggest discovery is [vim-easymotion](https://github.com/Lokaltog/vim-easymotion) though, perfect for jumping within long texts like this blog article. Just a few weeks ago an Emacs fanatic coworker was showing off his setup with [AceJump](http://www.emacswiki.org/emacs/AceJump).

This is what my revamped Vim in tmux setup looks like:
![screen shot]({filename}images/dotfiles2.png)
