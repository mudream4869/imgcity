import asyncio
import os

import aiofiles
from redis import Redis

from app.markdown import markdownToHTML


class PikiReader:
    PATH_CHARS = 'abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWXZY0123456789-_/'

    def __init__(self, redis_client: Redis, piki_root: str):
        self.redis_client = redis_client
        self.piki_root = piki_root

    def _check_path(self, path):
        """
            Check path:
                - should only contain: a-zA-Z0-9-_/
                - length < 255
        """
        for ch in path:
            if ch not in PikiReader.PATH_CHARS:
                return False
        return True

    async def _get_piki(self, path: str):
        """
            path = /a/c/b:  return /a/c/b.md
            path = /a/c/b/: return /a/c/b/README.md
        """
        if path.endswith('/') or path == '':
            path += 'README.md'
        else:
            path += '/README.md'

        path = os.path.join(self.piki_root, path)

        async with aiofiles.open(path, mode='r') as f:
            return await f.read()

    async def get_piki(self, path: str):
        if not self._check_path(path):
            raise RuntimeError(f'{path} is not secure')

        content = self.redis_client.hget('imgcity:piki', path)
        if content:
            return content.decode('utf-8')

        content = await self._get_piki(path)
        content = markdownToHTML(content)
        self.redis_client.hset('imgcity:piki', path, content)
        return content
