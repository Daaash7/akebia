from typing import List

from app.cart.models import CartPosition
from app.price.accessor import get_current_price
from app.products.accessor import get_product_by_id
from app.store.database import db
from app.warehouse.accessor import get_product_count


async def add_to_cart(user_id, product_id, count):
    try:
        await db.execute("INSERT INTO carts (product_id, user_id, count) VALUES ($1, $2, $3)", product_id, user_id, count)
        return True
    except Exception as e:
        print(e)
        return False

async def check_product_in_cart(product_id, user_id):
    res = await db.fetch("SELECT * FROM carts WHERE product_id = $1 AND user_id = $2", product_id, user_id)
    if len(res) == 0:
        return False
    return True

async def del_from_cart(user_id: int, product_id: int):
    await db.execute("DELETE FROM carts WHERE product_id = $1 AND user_id = $2", product_id, user_id)

async def del_all_cart(user_id: int):
    await db.execute("DELETE FROM carts WHERE user_id = $1", user_id)

async def get_all_cart(user_id) -> List[CartPosition]:
    res = await db.fetch("SELECT * FROM carts WHERE user_id = $1 LIMIT 10;", user_id)
    data = []
    for rec in res:
        pr_id = rec["product_id"]
        product = await get_product_by_id(pr_id)
        price = await get_current_price(pr_id)
        if not price:
            continue
        card = CartPosition(
            product,
            price,
            await get_product_count(pr_id)
        )
        data.append(card)
    return data
