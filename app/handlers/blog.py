from tornado import web

from app.handlers.base import RequestHandler


class BlogHandler(RequestHandler):
    async def get(self, year, month, day, name):
        try:
            full_name = f'blog/{year}/{month}/{day}/{name}'
            content = await self.blog_reader.get_blog(year, month, day, name)
            self.render('blogpost.html',
                        content=content,
                        full_name=full_name,
                        github_comment_source=self.github_comment_source)
        except FileNotFoundError:
            raise web.HTTPError(404)


class BlogFileHandler(web.StaticFileHandler):
    async def get(self, year, month, day, name, include_body=True):
        path = f'{year}/{month}/{day}/{name}'
        return await super().get(path, include_body)


class BlogIndexHandler(RequestHandler):
    async def get(self):
        tag = self.get_argument('tag', None)
        blogpost_list = self.blog_reader.blog_list
        if tag:
            new_list = []
            for blog in blogpost_list:
                if tag in blog['tags']:
                    new_list.append(blog)
            blogpost_list = new_list

        self.render('blog_list.html',
                    blogpost_list=blogpost_list,
                    tags_count=self.blog_reader.tags_count)
