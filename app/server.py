import os

import redis
import tornado.ioloop
from tornado import web

from app import blog, piki
from app.handlers import (BlogFileHandler, BlogHandler, BlogIndexHandler,
                          MainHandler, PikiFileHandler, PikiHandler)


def make_app():
    redis_client = redis.Redis()
    piki_root = 'data/piki'
    blog_root = 'data/blog'

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
        'debug': True,
        'cookie_secret': 'abcde',
        'static_path': os.path.join(file_dir, "static"),
        'template_path': os.path.join(file_dir, "templates")
    }

    return tornado.web.Application([
        (r'/', MainHandler, args),
        (r'/blog/', BlogIndexHandler, args),
        (r'/blog/(\d{4})-(\d{2})-(\d{2})/(.*)/', BlogHandler, args),
        (r'/blog/(\d{4})-(\d{2})-(\d{2})/(.*)',
         BlogFileHandler, {'path': blog_root}),

        (r'/piki/', web.RedirectHandler, {"url": "/piki/index/"}),
        (r'/piki/(.*)/', PikiHandler, args),
        (r'/piki/(.*)', PikiFileHandler, {'path': piki_root}),
    ], **setting)


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)

    print('Start listening port', 8888)
    tornado.ioloop.IOLoop.current().start()
