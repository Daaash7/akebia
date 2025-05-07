from datetime import datetime

from pydantic.dataclasses import dataclass


@dataclass
class Price:
    id: int
    date: datetime
    product_id: int
    price: int | None
