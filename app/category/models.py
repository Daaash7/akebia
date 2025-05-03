from pydantic.dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str
