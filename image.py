from typing import Union
from pathlib import Path
import config
from PIL import Image

class ChangeImage:
    def __init__(self):
        self.max_size = config.max_sticker_size

    def reduce_image_size(self, image: Union[str, Path]) -> Image:
        """
        Reduces the size of an image.

        :param image: Path to the image file as a string or a Path object, or an instance of the PIL Image class.
        :return: A resized PIL Image object.

        This function takes an image file path or a PIL Image object and resizes it to fit within the specified maximum size (self.max_size).
        If the image provided is already an instance of the PIL Image class, it resizes the image in place.
        If the provided image exceeds the maximum size, it opens the image, resizes it, and returns the resized image.

        :param image: Path to the image file as a string or a Path object, or an instance of the PIL Image class.
        :return: A resized PIL Image object.
        """
        # If Image - PIL.Image
        if isinstance(image, Image.Image):
            image.thumbnail(self.max_size)
            return image

        # If Image - Path or str
        if isinstance(image, (str, Path)):
            image_path = str(image)  # Преобразуем в строку, если это Path
            with Image.open(image_path) as img:
                img.thumbnail(self.max_size)
                return img

        raise ValueError("Unsupported image type. Please provide an image file path or a PIL Image object.")
