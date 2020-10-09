import asyncio
import os

import aiofiles
import redis
import yaml

from app.markdown import markdownToHTML, abbrMarkdownHTML

HOUR = 60 * 60


class BlogReader:
    def __init__(self, redis_client: redis.Redis, blog_root: str):
        self.redis_client = redis_client
        self.blog_root = blog_root

        self.blog_list = self._get_blog_list()

    def _is_legal_date(self, year: str, month: str, day: str) -> bool:
        if len(year) != 4 or len(month) != 2 or len(day) != 2:
            return False

        iyear = int(year)
        if iyear < 0:
            return False

        imonth = int(month)
        iday = int(day)
        MONTHDAY = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if iday <= 0 or iday > MONTHDAY[imonth - 1]:
            return False

        return True

    def _get_blog_list(self):
        """
            Load blog list

            File format:
            - datetime: YYYY-MM-DD HH:MM:SS
              filename: (string)
              title: (string)

            Return: [
                {
                    datetime: YYYY-MM-DD
                    filename: <blog filename>
                    title: <blog title>
                }, ...
            ]
        """
        path = os.path.join(self.blog_root, 'blog.yaml')
        with open(path, 'r') as f:
            blogitems = yaml.safe_load(f)
            blogitems.sort(key=lambda x: x['datetime'], reverse=True)
            for item in blogitems:
                dt = item['datetime']
                item['datetime'] = '%04d-%02d-%02d' % (
                    dt.year, dt.month, dt.day)

                syear = '%04d' % dt.year
                smonth = '%02d' % dt.month
                sday = '%02d' % dt.day

                item['abstract'] = self._get_blog_abbr(
                    syear, smonth, sday, item['filename'])
            return blogitems

    async def _get_blog(self, year: str, month: str, day: str, name: str):
        path = f'{year}/{month}/{day}/{name}/README.md'
        path = os.path.join(self.blog_root, path)

        async with aiofiles.open(path, mode='r') as f:
            return await f.read()

    def _get_blog_noasync(self, year: str, month: str, day: str, name: str):
        path = f'{year}/{month}/{day}/{name}/README.md'
        path = os.path.join(self.blog_root, path)

        with open(path, mode='r') as f:
            return f.read()

    def _get_blog_abbr(self, year: str, month: str, day: str, name: str):
        content = self._get_blog_noasync(year, month, day, name)
        return abbrMarkdownHTML(content)

    async def get_blog(self, year: str, month: str, day: str, name: str):
        if not self._is_legal_date(year, month, day):
            raise RuntimeError(f'parameter error: {year}/{month}/{day}')

        redis_key = f'{year}-{month}-{day}@{name}'

        content = self.redis_client.hget('imgcity:blog', redis_key)
        if content:
            return content.decode('utf-8')

        content = await self._get_blog(year, month, day, name)
        content = markdownToHTML(content)
        self.redis_client.hset('imgcity:blog', redis_key, content)
        return content
