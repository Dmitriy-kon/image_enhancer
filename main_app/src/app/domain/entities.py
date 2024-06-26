from dataclasses import dataclass
from pathlib import Path


@dataclass
class Image:
    name: str
    url: str
    convert_data: dict

    def get_updated_name(self, new_filename: str) -> str:
        new_filename = new_filename.replace(" ", "_")
        new_filename, old_filename = Path(new_filename), Path(self.name)
        self.name = new_filename.with_suffix(old_filename.suffix).name

    @staticmethod
    def create(name: str, convert_data: dict | None = None, url: str = "") -> "Image":
        return Image(name, url, convert_data)
