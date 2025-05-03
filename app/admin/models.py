from dataclasses import asdict

from pydantic.dataclasses import dataclass


@dataclass
class Admin:
    id: int
    name: str
    password: str

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}