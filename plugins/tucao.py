#coding=utf-8
from tornado.escape import json_decode
from tornado.util import ObjectDict
import dbhash as dbm
import jieba.analyse
import time
import logging

__name__ = 'tucao'

DB = dbm.open("tucao.db","c")

def test(data, msg=None, bot=None):
    data = data.strip()
    if data == 'tc' or data.startswith("tc "):
        return True
    return False  

def respond(data, msg=None, bot=None):  
    idata = data.strip()
    result = []
    if idata == 'tc':
        try:
            keys = DB.keys()
            keys.sort()
            keys.reverse()
            for k in keys:
                if len(result) >= 5:break
                result.append(">> %s"%DB[k])
        except Exception, e:
            raise e
    elif idata.startswith("tc "):
        tct = idata[3:]
        tct = isinstance(tct, unicode) and tct.encode("utf-8") or tct
        if len(tct) < 8:
            return u"这也算吐槽？至少8个字吧。"

        try:
            key = '%s'%time.time()
            DB[key] = tct
            DB.sync()
            tags1 = set(jieba.analyse.extract_tags(tct,20))
            for k,v in DB.iteritems():
                if key == k:continue
                if len(result) >= 5:break
                _tags = set(jieba.analyse.extract_tags(v,20))
                if tags1.intersection(_tags):
                    result.append(">> %s"%v)
        except Exception, e:
            logging.error(e)
            raise e

    if not result:
        return u"知音难求，吐槽也寂寞啊。"

    return "\n".join(result)

        



if __name__ == '__main__':
    print '----------------'
    import jieba.analyse
    a = u"话说很好奇他卖的究竟是怎样的东西python。感觉国内的贩子都好厉害。"
    b = u"会不会是偷的？曾经有看到过无敌兔有卖5k不到的。python 感觉是偷的？"
    aa = set(jieba.analyse.extract_tags(a,20))
    bb = set(jieba.analyse.extract_tags(b,20))
    cc = aa.intersection(bb)
    print ','.join(list(aa))
    print ','.join(list(bb))
    print ','.join(list(cc))