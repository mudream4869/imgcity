import redis
import tornado

from app import blog, piki


class RequestHandler(tornado.web.RequestHandler):
    def initialize(self,
                   redis_client: redis.Redis,
                   piki_reader: piki.PikiReader,
                   blog_reader: blog.BlogReader,
                   github_comment_url: str):

        self.redis_client = redis_client
        self.piki_reader = piki_reader
        self.blog_reader = blog_reader
        self.github_comment_url = github_comment_url
