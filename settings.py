#coding=utf-8
import os
from tornado.options import options, define

APPDIR = os.path.abspath(os.path.dirname(__file__))


MSG_TYPE_TEXT = u'text'
MSG_TYPE_LOCATION = u'location'
MSG_TYPE_IMAGE = u'image'
MSG_TYPE_LINK = u'link'
MSG_TYPE_EVENT = u'event'

MSG_TYPE_MUSIC = u'music'
MSG_TYPE_NEWS = u'news'


def init():
    define('debug', type=bool, default=True, help='application in debug mode?')
    define('port', type=int, default=8000,help='the port application listen to')
    define('token', type=str, default='talk1979', help='your wechat token')
    define('username', type=str, default='', help='your wechat username')
    define('simsimi_key', type=str, default='2352474b-7b3e-4e5d-a08f-ed9a3feeba63', help='simsimi api key')
    define('feed_url', type=str, default='http://blog.csdn.net/talkincode/rss/list', help='rss feed url')
