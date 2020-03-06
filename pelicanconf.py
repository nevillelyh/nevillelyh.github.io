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
SOCIAL = (('Spotify', 'https://open.spotify.com/user/sinisa_lyh'),
          ('GitHub', 'https://github.com/nevillelyh'),
          ('Twitter', 'https://twitter.com/sinisa_lyh'),
          ('SlideShare', 'https://www.slideshare.net/sinisalyh'),
          ('YouTube', 'https://www.youtube.com/user/sinisalyh/videos'),
          ('Instagram', 'https://www.instagram.com/sinisa/'),
          ('Flickr', 'https://www.flickr.com/photos/sinisa_lyh'),
          )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

FEED_DOMAIN = SITEURL
TWITTER_USERNAME = 'sinisa_lyh'
TWITTER_WIDGET_ID = '887720870931726336'
THEME = 'pelican-themes/pelican-bootstrap3'
TYPOGRIFY = True

# pelican-bootstrap3
ABOUT_ME = '''
Data infrastructure @<a href="https://twitter.com/Spotify">Spotify</a>, ex-@<a href="https://twitter.com/Yahoo">Yahoo</a> search, das keyboard shredder, author of <a href="https://github.com/spotify/scio">Scio</a>
'''
AVATAR = ('/avatar.jpg')
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

SUMMARY_MAX_LENGTH = 200
# pelican-bootstrap3
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['i18n_subsites']
