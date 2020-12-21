import io
import os

import PIL.Image


class ImageFileHandler:
    def __init__(self, blog_root: str):
        self.blog_root = blog_root

    def list_image(self, filepath):
        full_filepath = os.path.join(self.blog_root, filepath)
        return [fn for fn in os.listdir(full_filepath)
                if fn.endswith(".png") or fn.endswith(".jpg") or fn.endswith(".gif")]

    def upload_image(self, filepath, filename, filebody):
        file_like = io.BytesIO(filebody)
        img = PIL.Image.open(file_like)
        file_with_path = os.path.join(self.blog_root, filepath, filename)
        print(file_with_path)
        img.save(file_with_path)

    def delete_image(self, filepath, filename):
        file_with_path = os.path.join(self.blog_root, filepath, filename)
        os.remove(file_with_path)
