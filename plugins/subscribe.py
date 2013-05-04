#coding=utf-8
import requests
from tornado.escape import json_decode
from tornado.util import ObjectDict

__name__ = 'subscribe'


def test(data, msg=None, bot=None):
    if 'subscribe' == data.strip():
        return True
    return False


def respond(data, msg=None, bot=None):  
    return '''欢迎关注《程序人生》\n
支持命令选项：\n
>> h  -- 显示帮助文档\n
>> oschina  -- 获取开源中国网站最新资讯\n
>> x.x.x.x  -- 输入ip地址可查询归属地\n
>> 更多功能完善中，敬请期待...


    '''