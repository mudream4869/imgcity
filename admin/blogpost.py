import datetime
import os
import shutil

import dateutil.parser
import yaml


class BlogpostHandler:
    def __init__(self, blog_root: str):
        self.blog_root = blog_root
        self.blog_yaml = os.path.join(self.blog_root, 'blog.yaml')
        self.pull_list()

    def _get_readme_path(self, filepath):
        return os.path.join(self.blog_root, filepath, 'README.md')

    def _get_dir_path(self, filepath):
        return os.path.join(self.blog_root, filepath)

    def pull_list(self):
        with open(self.blog_yaml, encoding='utf-8') as f:
            self.blogpost_list = yaml.safe_load(f.read())

    def push_list(self):
        with open(self.blog_yaml, 'w') as f:
            yaml.dump(self.blogpost_list, f,
                      default_flow_style=False, allow_unicode=True)

    def get_list(self):
        return self.blogpost_list

    def _get_blogpost(self, filepath):
        part = filepath.split('/')
        to_match_date_tuple = tuple(map(int, part[0: 3]))
        to_match_filename = part[3]

        for blogpost in self.blogpost_list:
            dt = blogpost['datetime']
            date_tuple = (dt.year, dt.month, dt.day)
            if blogpost['filename'] == to_match_filename and date_tuple == to_match_date_tuple:
                return blogpost

        return None

    def get(self, filepath):
        blogpost = self._get_blogpost(filepath).copy()
        with open(self._get_readme_path(filepath)) as f:
            blogpost['md'] = f.read()

        return blogpost

    def update_post_md(self, filepath, md):
        with open(self._get_readme_path(filepath), 'w') as f:
            f.write(md)

    def update_post_title(self, filepath, title):
        blogpost = self._get_blogpost(filepath)
        blogpost['title'] = title
        self.push_list()

    def create_post(self, filepath):
        os.makedirs(self._get_dir_path(filepath), exist_ok=True)
        with open(self._get_readme_path(filepath), 'w') as f:
            f.write('# NoTitle')

        part = filepath.split('/')

        blogpost = {
            'filename': part[3],
            'title': part[3],
            'datetime': datetime.datetime(int(part[0]), int(part[1]), int(part[2]), 8, 0)
        }
        self.blogpost_list.append(blogpost)
        self.push_list()

        return None, blogpost

    def delete_post(self, filepath):
        blogpost = self._get_blogpost(filepath)
        self.blogpost_list.remove(blogpost)
        shutil.rmtree(self._get_dir_path(filepath))
        self.push_list()
