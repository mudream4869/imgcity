import datetime
import json
import os

import tornado.ioloop
import tornado.web

from admin import blogpost, image


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.time):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class RequestHandler(tornado.web.RequestHandler):
    def initialize(self,
                   blogpost_handler: blogpost.BlogpostHandler,
                   image_handler: image.ImageFileHandler):
        self.blogpost_handler = blogpost_handler
        self.image_file_handler = image_handler


class BlogListHandler(RequestHandler):
    def get(self):
        self.render('blogpost_list.html')


class BlogEditHandler(RequestHandler):
    def get(self, filepath):
        self.render('blogpost.html', filepath=filepath)


class BlogHandler(RequestHandler):
    def get(self, filepath):
        if not filepath:
            simple_list = []
            for bp in self.blogpost_handler.list():
                simple_list.append({
                    'title': bp['title'],
                    'filename': bp['filename'],
                    'datetime': bp['datetime'].isoformat(),
                })

            self.finish(json.dumps(simple_list))
        else:
            self.finish(json.dumps(self.blogpost_handler.get(
                filepath), cls=DateTimeEncoder))

    def post(self, filepath):
        err, blogpost = self.blogpost_handler.create_post(filepath)
        self.finish(err or json.dumps(blogpost, cls=DateTimeEncoder))

    def patch(self, filepath):
        md = self.get_argument('md', default=None)
        title = self.get_argument('title', default=None)

        if md is not None:
            self.blogpost_handler.update_post_md(filepath, md)

        if title is not None:
            self.blogpost_handler.update_post_title(filepath, title)

    def delete(self, filepath):
        self.blogpost_handler.delete_post(filepath)


class BlogServer(RequestHandler):
    def get(self, filepath):
        if not filepath:
            self.render('blogpost_list.html',
                        blogpost_list=self.blogpost_handler.list())
        else:
            self.render('blogpost.html',
                        filepath=filepath)


class ImageHandler(RequestHandler):
    def get(self, filepath):
        image_list = self.image_file_handler.list_image(filepath)
        self.finish(json.dumps(image_list))

    def post(self, filepath):
        upload_file = self.request.files['file'][0]
        filename = self.get_argument('filename')
        self.image_file_handler.upload_image(
            filepath, filename, upload_file['body'])

    def delete(self, filepath):
        filename = self.get_argument('filename')
        self.image_file_handler.delete_image(filepath, filename)


def make_app():
    blog_root = 'data/blog'
    blogpost_handler = blogpost.BlogpostHandler(blog_root)
    image_handler = image.ImageFileHandler(blog_root)

    args = {
        'blogpost_handler': blogpost_handler,
        'image_handler': image_handler,
    }

    file_dir = os.path.dirname(__file__)

    setting = {
        'debug': True,
        'cookie_secret': 'abcde',
        'static_path': os.path.join(file_dir, 'static'),
        'template_path': os.path.join(file_dir, 'templates')
    }

    return tornado.web.Application([
        (r'/api/blog/(.*)', BlogHandler, args),
        (r'/api/image/(.*)', ImageHandler, args),
        (r'/blog/(.*)', BlogServer, args),
        (r'/blogdb/(.*)', tornado.web.StaticFileHandler,
         {'path': blog_root}),
    ], **setting)


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)

    print('Start listening port', 8888)
    tornado.ioloop.IOLoop.current().start()
