from app.handlers.base import RequestHandler


class MainHandler(RequestHandler):
    async def get(self):
        self.render('index.html')
