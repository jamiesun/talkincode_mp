#coding=utf-8
import time
from tornado.util import ObjectDict
from tornado.options import options
from xml.etree import ElementTree
from settings import MSG_TYPE_TEXT,MSG_TYPE_LOCATION,MSG_TYPE_IMAGE,\
                     MSG_TYPE_LINK,MSG_TYPE_EVENT,MSG_TYPE_MUSIC,MSG_TYPE_NEWS


def decode(s):
    if isinstance(s, str):
        s = s.decode('utf-8')
    return s


def parse_msg(xml):
    if not xml:
        return None
    parser = ElementTree.fromstring(xml)
    id_node = parser.find('MsgId')
    msg_id = id_node and int(id_node.text) or 0
    msg_type = decode(parser.find('MsgType').text)
    touser = decode(parser.find('ToUserName').text)
    fromuser = decode(parser.find('FromUserName').text)
    create_at = int(parser.find('CreateTime').text)
    msg = ObjectDict(
        mid=msg_id,
        type=msg_type,
        touser=touser,
        fromuser=fromuser,
        time=create_at
    )
    if msg_type == MSG_TYPE_TEXT:
        msg.content = decode(parser.find('Content').text)
    elif msg_type == MSG_TYPE_LOCATION:
        msg.location_x = decode(parser.find('Location_X').text)
        msg.location_y = decode(parser.find('Location_Y').text)
        msg.scale = int(parser.find('Scale').text)
        msg.label = decode(parser.find('Label').text)
    elif msg_type == MSG_TYPE_IMAGE:
        msg.picurl = decode(parser.find('PicUrl').text)
    elif msg_type == MSG_TYPE_LINK:
        msg.title = decode(parser.find('Title').text)
        msg.description = decode(parser.find('Description').text)
        msg.url = decode(parser.find('Url').text)
    elif msg_type == MSG_TYPE_EVENT:
        msg.event = decode(parser.find('Event').text)
        msg.event_key = decode(parser.find('EventKey').text)
    return msg


def reply_text(fromuser, touser, text):
    tpl = """<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <FuncFlag>0</FuncFlag>
    </xml>
    """

    timestamp = int(time.time())
    return tpl % (touser, fromuser, timestamp, MSG_TYPE_TEXT, text)


def reply_music(fromuser, touser, music):
    tpl = """<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <Music>
    <Title><![CDATA[%s]]></Title>
    <Description><![CDATA[%s]]></Description>
    <MusicUrl><![CDATA[%s]]></MusicUrl>
    <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
    </Music>
    <FuncFlag>0</FuncFlag>
    </xml>
    """

    timestamp = int(time.time())
    return tpl % (touser, fromuser, timestamp, MSG_TYPE_MUSIC, 
                  music['titlle'],music['description'],music['music_url'],music['hq_music_url'])  


def reply_articles(fromuser, touser, articles):
    tpl = """<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <ArticleCount>%s</ArticleCount>
    <Articles>%s</Articles>
    <FuncFlag>0</FuncFlag>
    </xml>
    """
    itemtpl = """<item>
    <Title><![CDATA[%s]]></Title>
    <Description><![CDATA[%s]]></Description>
    <PicUrl><![CDATA[%s]]></PicUrl>
    <Url><![CDATA[%s]]></Url>
    </item>
    """

    timestamp = int(time.time())
    items = []
    if not isinstance(articles, list):
        articles = [articles]
    count = len(articles)
    for article in articles:
        item = itemtpl % (article['title'], article['description'],
                          article['picurl'], article['url'])
        items.append(item)
    article_str = '\n'.join(items)

    return tpl % (touser, fromuser, timestamp,MSG_TYPE_NEWS,
                  count, article_str)

def gen_reply(fromuser, touser, result):
    if result['msg_type'] == MSG_TYPE_NEWS:
        return reply_articles(fromuser, touser, result['response'])
    elif result['msg_type'] == MSG_TYPE_TEXT:
        return reply_text(fromuser, touser, result['response'])
    elif result['msg_type'] == MSG_TYPE_MUSIC:
        return reply_music(fromuser, touser, result['response'])