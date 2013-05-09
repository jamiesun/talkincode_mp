#coding=utf-8
import logging
import sender
import requests
from hashlib import sha1
from tornado.util import ObjectDict
from tornado import web
from tornado.options import options
from ai import AI 
from settings import MSG_TYPE_TEXT,MSG_TYPE_LOCATION,MSG_TYPE_IMAGE,\
                     MSG_TYPE_LINK,MSG_TYPE_EVENT,MSG_TYPE_MUSIC,MSG_TYPE_NEWS




def _simsimi(msg):
    errstr = u'思考混乱中，无法回答，回复h查看帮助。'
    if not msg:
        return None
    payload = {'text': msg, 'lc': 'ch','key':options.simsimi_key}
    headers = {'Content-Type': 'application/json; charset=utf-8',
               'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',}
    try:
        r = requests.get("http://sandbox.api.simsimi.com/request.p", params=payload)
        rt =  r.json()
        if options.debug:
            logging.info('simsimi response %s',str(rt))
        return "OK" in rt['msg'] and rt['response'] or errstr
    except:
        return errstr


class MsgProcess():

    def __init__(self,msg):
        self.msg = msg

    def process(self):
        if self.msg.type == MSG_TYPE_TEXT:
            return sender.gen_reply(self.msg.touser, self.msg.fromuser,  self.process_text())
        elif self.msg.type == MSG_TYPE_LOCATION:
            return sender.gen_reply(self.msg.touser, self.msg.fromuser,  self.process_location())
        elif self.msg.type == MSG_TYPE_IMAGE:
            return sender.gen_reply(self.msg.touser, self.msg.fromuser,  self.process_image())
        elif self.msg.type == MSG_TYPE_EVENT:
            return sender.gen_reply(self.msg.touser, self.msg.fromuser,  self.process_event())
        elif self.msg.type == MSG_TYPE_LINK:
            return sender.gen_reply(self.msg.touser, self.msg.fromuser,  self.process_link())
        else:
            logging.info('message type unknown') 

    def process_text(self):
        bot = AI(self.msg)
        print self.msg
        result = bot.respond(self.msg.content)
        if options.debug:
            logging.info('bot response %s',result)
        if isinstance(result, list):
            return ObjectDict(msg_type=MSG_TYPE_NEWS,response=result)
        else:
            return ObjectDict(msg_type=MSG_TYPE_TEXT,response=sender.decode(result))

    def process_event(self):
        pass

    def process_location():
        return process_nothing()

    def process_image():
        return process_nothing()

    def process_link():
        return process_nothing()

    def process_nothing():
        return ObjectDict(msg_type=MSG_TYPE_TEXT,response=u'人生苦短，不想废话')


class MainHandler(web.RequestHandler):
    def get_error_html(self, status_code, **kwargs):
        self.set_header("Content-Type", "application/xml;charset=utf-8")
        try:
            if self.touser and self.fromuser:
                reply = sender.reply_text(self.touser, self.fromuser,
                                               u'程序混乱中，无法回答，回复h查看帮助。')
                self.write(reply)
                return
        except:
            pass

    def check_signature(self):
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')

        tmparr = [options.token, timestamp, nonce]
        tmparr.sort()
        tmpstr = ''.join(tmparr)
        tmpstr = sha1(tmpstr).hexdigest()

        return tmpstr == signature


    def get(self):
        echostr = self.get_argument('echostr', '')
        if self.check_signature():
            self.write(echostr)
            logging.info("Signature check success.")
        else:
            logging.warning("Signature check failed.")



    def post(self):
        if not self.check_signature():
            logging.warning("Signature check failed.")
            return

        self.set_header("Content-Type", "application/xml;charset=utf-8")
        body = self.request.body
        msg = sender.parse_msg(body)
        if not msg:
            logging.info('Empty message, ignored')
            return

        if options.debug:
            logging.info('message type %s from %s with %s', msg.type,msg.fromuser,body)

        reply_msg = MsgProcess(msg).process()
        if options.debug:
            logging.info('Replied to %s with "%s"', msg.fromuser, reply_msg)

        self.write(reply_msg)




handlers = [
    ('/weixin', MainHandler),
]

if __name__ == '__main__':
    print _simsimi("hello")