import io
import os

import PIL.Image


class ImageFileHandler:
    IMAGE_FILE_EXTS = ['png', 'jpg', 'gif']

    def __init__(self, blog_root: str):
        self.blog_root = blog_root

    def _is_img(self, filename):
        for ext in self.IMAGE_FILE_EXTS:
            if filename.endswith('.' + ext):
                return True
        return False

    def list_image(self, filepath):
        full_filepath = os.path.join(self.blog_root, filepath)
        return [fn for fn in os.listdir(full_filepath) if self._is_img(fn)]

    def upload_image(self, filepath, filename, filebody):
        file_like = io.BytesIO(filebody)
        img = PIL.Image.open(file_like)
        file_with_path = os.path.join(self.blog_root, filepath, filename)
        img.save(file_with_path)

    def delete_image(self, filepath, filename):
        file_with_path = os.path.join(self.blog_root, filepath, filename)
        os.remove(file_with_path)
