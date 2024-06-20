import io

from entities.image import Image
from PIL import Image as Img
from PIL import ImageOps


class ImageProcessor:
    def __init__(self, image: Image) -> None:
        self.image = image

    def __enter__(self):
        self.img = Img.open(io.BytesIO(self.image.data))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.img.close()

    def grayscale(self):
        self.img = self.img.convert("L")

    def resize(self, width: int, height: int):
        self.img = ImageOps.contain(
            self.img, (width, height), method=Img.Resampling.LANCZOS
        )

    def save(self) -> Image:
        byte_array = io.BytesIO()

        self.img.save(byte_array, format="JPEG")
        self.image.data = byte_array.getvalue()
        return self.image
