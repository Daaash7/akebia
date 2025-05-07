from app.category.accessor import get_category_by_id
from app.manufacturers.accessor import get_manufacturer_by_id
from app.price.accessor import set_price, get_current_price
from app.products.models import Product, ProductCard
from app.store.database import db
from app.utils.utils import generate_article_number


async def get_products_by_category(category_id: int):
    res = await db.fetch("SELECT * FROM products WHERE category_id = $1", category_id)
    return [Product(**pr) for pr in res]

async def get_product_by_manufacturer(manufacturer_id: int):
    res = await db.fetch("SELECT * FROM products WHERE manufacturer_id = $1", manufacturer_id)
    return [Product(**pr) for pr in res]

async def create_product(name: str, description: str, category_id: int, image_filename: str, product_price: int) -> Product | None:
    try:
        res = await db.fetchrow("INSERT INTO products (name, product_code, description, manufacturer_id, category_id, image_filename) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *", name, generate_article_number(), description, 0, category_id, image_filename)
        product_id = res["id"]
        pr = await get_product_by_id(product_id)
        await set_price(pr.id, product_price)
        return pr
    except Exception as e:
        print(e)
        return None

async def get_product_by_id(product_id: int) -> Product:
    res = await db.fetchrow("SELECT * FROM products WHERE id = $1", product_id)
    if res is not None:
        return Product(**res)

async def get_new_collection():
    res = await db.fetch("SELECT * FROM new_collection")
    data = []
    for i in res:
        product_id = i.get("product_id")
        if product_id:
            product_el = await get_product_by_id(product_id)
            price = await get_current_price(product_id)
            manufacturer = await get_manufacturer_by_id(product_el.manufacturer_id)
            category = await get_category_by_id(product_el.category_id)
            data.append(
                ProductCard(
                    product_el,
                    price,
                    manufacturer,
                    category
                )
            )
    return data

async def is_new_collection(product_id: int) -> bool:
    res = await db.fetchrow("SELECT * FROM new_collection WHERE product_id = $1", product_id)
    if res is not None:
        return True
    return False

async def add_product_to_new_coll(product_id: int):
    try:
        await db.execute("INSERT INTO new_collection (product_id) VALUES ($1)", product_id)
        return True
    except Exception:
        return False

async def del_product_from_new_coll(product_id: int):
    try:
        await db.execute("DELETE FROM new_collection WHERE product_id=($1)", product_id)
        return True
    except Exception:
        return False