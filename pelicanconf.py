#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Neville Li'
SITENAME = u'Das Keyboard Shredder'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)
LINKS = ()

# Social widget
SOCIAL = (('Spotify', 'http://open.spotify.com/user/sinisa_lyh'),
          ('GitHub', 'https://github.com/nevillelyh'),
          ('Twitter', 'https://twitter.com/sinisa_lyh'),
          ('LinkedIn', 'https://www.linkedin.com/in/nevillelyh'),
          ('SlideShare', 'http://www.slideshare.net/sinisalyh'),
          ('Stack-Overflow',
           'http://stackoverflow.com/users/3880836/neville-li'),
          ('Facebook', 'https://www.facebook.com/neville.lyh'),
          ('Google+', 'https://plus.google.com/+NevilleLiYH'),
          ('YouTube', 'https://www.youtube.com/user/sinisalyh/videos'),
          ('Flickr', 'https://www.flickr.com/photos/sinisa_lyh'),
          )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

FEED_DOMAIN = SITEURL
TWITTER_USERNAME = 'sinisa_lyh'
THEME = 'theme'
TYPOGRIFY = True

# pelican-bootstrap3
ABOUT_ME = '''
Data infrastructure @<a href="https://twitter.com/Spotify">Spotify</a>, ex-@<a href="https://twitter.com/Yahoo">Yahoo</a> search, das keyboard shredder, author of <a href="https://github.com/spotify/scio">Scio</a>
'''
# AVATAR = ('https://en.gravatar.com/userimage/'
#           '617848/35e202c9eea4168a35703a4c40f57473.jpg')
ADDTHIS_PROFILE = 'sinisalyh'
# GITHUB_USER = 'nevillelyh'
# GITHUB_SHOW_USER_LINK=True
DISPLAY_ARTICLE_INFO_ON_INDEX = True
SHOW_ARTICLE_CATEGORY = True
# SHOW_ARTICLE_AUTHOR = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
CC_LICENSE = 'CC-BY-NC'
PYGMENTS_STYLE = 'monokai'
