from dataclasses import dataclass, field


@dataclass
class Image:
    name: str
    data: bytes
    convert_data: "ImageDataConvert"

    @staticmethod
    def create(name: str, data: bytes, convert_data: dict | None = None) -> "Image":
        grayscale = convert_data.get("grayscale", False)
        scale = convert_data.get("scale", None)
        saturation = convert_data.get("saturation", 0)
        contrast = convert_data.get("contrast", 0)
        brightness = convert_data.get("brightness", 0)

        convert_data = ImageDataConvert.create(
            grayscale, scale, saturation, contrast, brightness
        )

        return Image(name, data, convert_data)


@dataclass
class ImageDataConvert:
    grayscale: bool
    scale: "ImageDataScale"
    saturation: int
    contrast: int
    brightness: int

    @staticmethod
    def create(
        grayscale: bool, scale: dict, saturation: int, contrast: int, brightness: int
    ) -> "ImageDataConvert":
        image_data_scale = ImageDataScale.create(scale["width"], scale["height"])
        return ImageDataConvert(
            grayscale, image_data_scale, saturation, contrast, brightness
        )

    def __repr__(self) -> str:
        return f"ImageDataConvert(grayscale={self.grayscale}, scale={self.scale}, saturation={self.saturation}, contrast={self.contrast}, brightness={self.brightness})"


@dataclass
class ImageDataScale:
    width: int
    height: int

    @staticmethod
    def create(width: int, height: int) -> "ImageDataScale":
        return ImageDataScale(width, height)
    
    def __repr__(self) -> str:
        return f"ImageDataScale(width={self.width}, height={self.height})"
