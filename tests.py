#coding=utf-8
import requests
import sys


def send_text(msg):
    tpl = u'''<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName> 
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[%s]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>
    '''
    xml = tpl%(msg)
    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    print requests.post('http://127.0.0.1:8000/weixin', data=xml, headers=headers).text

if __name__ == '__main__':
    send_text(unicode(sys.argv[1],'utf-8'))