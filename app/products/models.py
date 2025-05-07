from pydantic.dataclasses import dataclass

from app.category.models import Category
from app.manufacturers.models import Manufacturer
from app.price.models import Price


@dataclass
class Product:
    id: int
    name: str
    product_code: int
    description: str
    manufacturer_id: int
    category_id: int
    image_filename: str

@dataclass
class ProductCard:
    product: Product
    new_price: Price | None
    manufacturer: Manufacturer | None
    category: Category | None