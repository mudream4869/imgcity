from tornado import web

from app.handlers.base import RequestHandler


class BlogHandler(RequestHandler):
    async def get(self, year, month, day, name):
        try:
            content = await self.blog_reader.get_blog(year, month, day, name)
            self.render('blogpost.html', content=content)
        except FileNotFoundError:
            raise web.HTTPError(404)


class BlogFileHandler(web.StaticFileHandler):
    async def get(self, year, month, day, name, include_body=True):
        path = f'{year}/{month}/{day}/{name}'
        return await super().get(path, include_body)


class BlogIndexHandler(RequestHandler):
    async def get(self):
        self.render('blog_list.html', blogpost_list=self.blog_reader.blog_list)
