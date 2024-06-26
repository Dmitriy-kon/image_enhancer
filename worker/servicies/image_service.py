from adapters.pillow.image_processor import ImageProcessor
from adapters.s3.s3 import s3_storage_inner
from entities.image import Image
from faststream.nats.annotations import ObjectStorage


class ImageService:
    def __init__(self, object_storage: ObjectStorage) -> None:
        self.object_storage = object_storage

    async def get_image(self, filename: str) -> Image:
        file = await self.object_storage.get(filename)
        headers = file.info.headers
        return Image.create(filename, file.data, headers)

    def process_image(self, image: Image) -> Image:
        image_processor = ImageProcessor(image)
        res_image: Image = None

        with image_processor as ims:
            if image.convert_data.grayscale:
                ims.grayscale()
            if image.convert_data.scale:
                ims.resize(
                    image.convert_data.scale.width,
                    image.convert_data.scale.height,
                )
            if image.convert_data.saturation:
                ims.add_saturation(image.convert_data.saturation)
            if image.convert_data.contrast:
                ims.add_contrast(image.convert_data.contrast)
            if image.convert_data.brightness:
                ims.add_brightness(image.convert_data.brightness)
            res_image = ims.save()

        return res_image

    async def put_image(self, image: Image):
        print(image.name)
        await s3_storage_inner.upload_file(image.name, image.data)
