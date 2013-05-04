#!/usr/bin/env python
#coding=utf-8
import sys
import os
import logging
import settings

from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options, define
from tornado.options import parse_command_line

settings.init()

class Application(web.Application):

    def __init__(self):
        from handlers import handlers
        config = dict(
            debug=options.debug,
            autoescape=None
        )
        super(Application, self).__init__(handlers, **config)


def main():
    parse_command_line()
    if options.debug:
        logging.info('Starting server at port %s in debug mode' % options.port)
    else:
        logging.info('Starting server at port %s' % options.port)

    server = HTTPServer(Application(), xheaders=True)
    server.listen(int(options.port),'0.0.0.0')
    IOLoop.instance().start()

if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting application")