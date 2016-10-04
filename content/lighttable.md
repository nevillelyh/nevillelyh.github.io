Title: Light Table
Date: 2014-07-28 12:01AM
Category: code
Tags: clojure, intellij-idea, light-table

I recently picked up [Light Table](http://www.lighttable.com/) for [Clojure](http://clojure.org/) development and liked it. Form evaluation works out of the box and indentation is better than that in [La Clojure](http://plugins.jetbrains.com/plugin/?id=4050) plugin for [IntelliJ IDEA](http://www.jetbrains.com/idea/).

I particularly like the idea of command bar, which allows you to search for Light Table commands by name and execute them quickly. I was already used to IDEA's key map though (`Mac OS X 10.5+` which is more natural to Mac users than the default `Mac OS X`), and wanted something similar. The setting files are in Clojure so it's easy to customize. This is what I got so far for `user.keymap`:

```clojure
{:+ {:app {"alt-space" [:show-commandbar-transient]}

     :editor {"alt-w" [:editor.watch.watch-selection]
              "alt-shift-w" [:editor.watch.unwatch]
              "ctrl-alt-i" [:smart-indent-selection]
              "ctrl-alt-c" [:toggle-console]
              "ctrl-shift-j" [:editor.sublime.joinLines]
              "pmeta-d" [:editor.sublime.duplicateLine]
              "pmeta-shift-up" [:editor.sublime.swapLineUp]
              "pmeta-shift-down" [:editor.sublime.swapLineDown]
              "pmeta-/" [:toggle-comment-selection :editor.line-down]}}}
```

Apart from these, I found myself using `"pmeta-enter" [:eval-editor-form]` and `"ctrl-d" [:editor.doc.toggle]` most when writing Clojure code. After all they are probably the most essential ones no matter what editor you use :)
