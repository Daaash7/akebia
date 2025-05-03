from app.store.database import db


async def add_deliver(product_id: int, count) -> bool:
    try:
        await db.execute("INSERT INTO delievers (product_id, count) VALUES (?, ?)", (product_id, count))
        return True
    except Exception:
        return False

async def get_product_count(product_id: int) -> int:
    warehouse = (await db.fetchrow("SELECT sum(count) from deliveries where product_id = $1", product_id)).get('sum')
    if not warehouse:
        return 0
    sales = (await db.fetchrow("SELECT sum(count) from sales where product_id = $1", product_id)).get('sum')
    if not sales:
        return warehouse

    return warehouse - sales

async def add_new_sale(product_id, order_id, count = 1) -> bool:
    try:
        if await get_product_count(product_id) >= count:
            await db.execute("INSERT INTO sales (order_id, product_id, count) VALUES ($1, $2, $3)", order_id, product_id, count)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False