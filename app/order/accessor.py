from typing import List

from app.order.models import Order, Position
from app.price.accessor import get_price_for_date
from app.products.accessor import get_product_by_id
from app.store.database import db
from app.user.accessor import get_user_by_id


async def zip_orders(data):
    if not data:
        return []
    orders = []
    for order in data:
        products = await db.fetch("SELECT * FROM sales WHERE order_id=$1", order['id'])
        positions = []
        for product in products:
            product = await get_product_by_id(product['product_id'])
            price = await get_price_for_date(product.id, order['date'])
            positions.append(Position(product=product, price=price))
        orders.append(Order(id=order['id'],
                            positions=positions,
                            user=await get_user_by_id(order['user_id']),
                            address=order['address'],
                            date=order['date'],
                            status=await get_order_status(order['id'])
                            ))
    return orders

async def get_all_orders(user_id: int) -> List[Order]:
    res = await db.fetch("SELECT * FROM orders WHERE user_id=$1 ORDER BY date DESC LIMIT 3", user_id)
    return await zip_orders(res)

async def get_all_orders_admin() -> List[Order]:
    res = await db.fetch("SELECT * FROM orders ORDER BY date DESC")
    return await zip_orders(res)

async def get_order(order_id: int, user_id: int) -> Order:
    order = await db.fetchrow("SELECT * FROM orders WHERE user_id=$1 LIMIT 1", user_id)
    products = await db.fetch("SELECT * FROM sales WHERE order_id=$1", order['id'])
    positions = []
    for product in products:
        product = await get_product_by_id(product['product_id'])
        price = await get_price_for_date(product.id, order['date'])
        positions.append(Position(product=product, price=price))
    return Order(id=order['id'],
                        positions=positions,
                        user=await get_user_by_id(user_id),
                        address=order['address'],
                        date=order['date'],
                        status= await get_order_status(order['id']),
                        )

async def add_new_order(user_id: int, address: str) -> int:
    await db.execute("INSERT INTO orders (user_id, address) VALUES ($1, $2)", user_id, address)

    order_id = await db.fetchrow("SELECT id FROM orders WHERE user_id=$1 ORDER BY date DESC LIMIT 1;", user_id)
    await set_order_status(order_id.get("id"))
    return order_id.get("id")

async def get_order_status(order_id: int):
    res = await db.fetchrow("SELECT status FROM order_statuses WHERE order_id=$1 ORDER BY date DESC LIMIT 1;", order_id)

    return res.get("status") if res else None

async def set_order_status(order_id: int, status_id: int = 1):
    await db.execute("INSERT INTO order_statuses (order_id, status) VALUES ($1, $2)", order_id, status_id)