import os
import sys

import redis
import tornado.ioloop
from tornado import web

import yaml

from app import blog, piki
from app.handlers import (BlogFileHandler, BlogHandler, BlogIndexHandler,
                          MainHandler, PikiFileHandler, PikiHandler)


def make_app(config):
    srv_conf = config['server']

    redis_client = redis.Redis()
    piki_root = srv_conf['piki_root']
    blog_root = srv_conf['blog_root']

    piki_reader = piki.PikiReader(
        redis_client=redis_client, piki_root=piki_root)

    blog_reader = blog.BlogReader(
        redis_client=redis_client, blog_root=blog_root)

    args = {
        'redis_client': redis_client,
        'piki_reader': piki_reader,
        'blog_reader': blog_reader,
    }

    file_dir = os.path.dirname(__file__)

    setting = {
        'debug': srv_conf.get('debug', False),
        'cookie_secret': srv_conf['cookie_secret'],
        'static_path': os.path.join(file_dir, 'static'),
        'template_path': os.path.join(file_dir, 'templates')
    }

    return tornado.web.Application([
        (r'/', MainHandler, args),
        (r'/blog/', BlogIndexHandler, args),
        (r'/blog/(\d{4})-(\d{2})-(\d{2})/(.*)/', BlogHandler, args),
        (r'/blog/(\d{4})-(\d{2})-(\d{2})/(.*)',
         BlogFileHandler, {'path': blog_root}),

        (r'/piki/', web.RedirectHandler, {'url': '/piki/index/'}),
        (r'/piki/(.*)/', PikiHandler, args),
        (r'/piki/(.*)', PikiFileHandler, {'path': piki_root}),
    ], **setting)


if __name__ == '__main__':
    with open(sys.argv[1]) as fp:
        config = yaml.safe_load(fp)

    app = make_app(config)

    port = config['server']['port']
    app.listen(port)

    print('Start listening port', port)
    tornado.ioloop.IOLoop.current().start()
