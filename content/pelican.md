Title: First (real) post with Pelican
Date: 2014-07-26 10:47PM
Category: code
Tags: pelican, python, virtualenv

Finally decided to jump (back) on the blogging bandwagon. This time I decided to use a static site generator, since that seems the cool thing to do these days, and found this [site](https://www.staticgen.com/). I want something in a language I know well, so Ruby or JavaScript is out. It should also be actively maintained, so Scala is out since [monkeyman](https://github.com/wspringer/monkeyman), the only entry there, seems abandoned. I eventually settled on [Pelican](http://blog.getpelican.com/), the top ranked Python framework.

I set up a new [virtualenv](http://virtualenv.readthedocs.org/en/latest/) with [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) and also discovered [autoenv](https://github.com/kennethreitz/autoenv) along the way. It was easy to get started with the `pelican-quickstart` script and in a few minutes I have a working site already. Next I went shopping for themes in [pelican-themes](https://github.com/getpelican/pelican-themes) and picked [pelican-bootstrap3](https://github.com/DandyDev/pelican-bootstrap3.git). Turns out it doesn't work with [Spotify](https://www.spotify.com) icon yet so I forked the repo and made a quick [PR](https://github.com/DandyDev/pelican-bootstrap3/pull/115).

After some further tweaking with the settings I was pretty happy with the results. I went on to set up [Disqus](https://disqus.com/) and [Google Analytics](http://www.google.com/analytics/) for the site, and published it to my [Linode](https://www.linode.com/) with `make ssh_upload`.
