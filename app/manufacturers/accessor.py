
from app.manufacturers.models import Manufacturer
from app.store.database import db


async def get_all_manufacturers():
    res = await db.fetch("SELECT * FROM manufacturers")
    return [Manufacturer(**man) for man in res]


async def get_manufacturer_by_id(manufacturer_id):
    res = await db.fetchrow(f"SELECT * FROM manufacturers WHERE id={manufacturer_id}")
    if res:
        return Manufacturer(**res)
    return None


async def create_manufacturer(name, image_filename) -> Manufacturer:
    try:
        await db.execute("INSERT INTO manufacturers (name, image_filename) VALUES ($1, $2)", name, image_filename)
    except Exception as e:
        print(e)
        return None
    man = await db.fetchrow("SELECT * FROM manufacturers WHERE name = $1", name)
    return Manufacturer(**man)
