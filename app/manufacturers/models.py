from pydantic.dataclasses import dataclass

@dataclass
class Manufacturer:
    id: int
    name: str
    image_filename: str