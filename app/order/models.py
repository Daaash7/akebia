from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from app.price.models import Price
from app.products.models import Product
from app.user.models import User

class OrderStatus(Enum):
    PROCESSING = 1
    IN_ASSEMBLY = 2
    READY = 3

@dataclass
class Position:
    product: Product
    price: Price

@dataclass
class Order:
    id: int
    positions: List[Position]
    user: User
    address: str
    date: datetime
    status: str



