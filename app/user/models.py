from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    phone_number: str
    password: str
    registration_date: datetime