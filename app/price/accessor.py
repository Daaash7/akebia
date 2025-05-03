from datetime import datetime

from app.price.models import Price
from app.store.database import db


async def set_price(product_id: int, price: int):
    await db.execute("INSERT INTO price_changes (product_id, price) VALUES ($1, $2)", product_id, price)

async def get_current_price(product_id: int):
    res = await db.fetchrow("SELECT * FROM price_changes WHERE product_id = $1 ORDER BY date DESC", product_id)
    return Price(**res)

async def get_price_for_date(product_id: int, date: datetime) -> Price | None:
    res = await db.fetchrow("""SELECT * 
                                FROM price_changes 
                                WHERE product_id = $1 
                                AND date <= $2
                                ORDER BY date DESC
                                LIMIT 1;""",
                            product_id, date)
    if not res:
        return None
    return Price(**res)

