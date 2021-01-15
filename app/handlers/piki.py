from tornado import web

from app.handlers.base import RequestHandler


class PikiHandler(RequestHandler):
    async def get(self, path):
        level = path.split('/')
        prelevel = '/piki/'
        breadcrumb = []
        for i, lv in enumerate(level):
            prelevel += lv + '/'
            breadcrumb.append({
                'text': lv,
                'link': prelevel,
            })

        try:
            full_name = f'piki/{path}'
            content = await self.piki_reader.get_piki(path)
            self.render('piki.html',
                content=content,
                breadcrumb=breadcrumb,
                full_name=full_name,
                github_comment_url=self.github_comment_url)
        except FileNotFoundError:
            raise web.HTTPError(404)


class PikiFileHandler(web.StaticFileHandler):
    async def get(self, path, include_body=True):
        return await super().get(path, include_body)
