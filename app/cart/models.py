from pydantic.dataclasses import dataclass

from app.price.models import Price
from app.products.models import Product


@dataclass
class CartPosition:
    product: Product
    new_price: Price
    count: int