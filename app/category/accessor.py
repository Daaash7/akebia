
from app.category.models import Category
from app.store.database import db


async def get_all_categories():
    res = await db.fetch("SELECT * FROM categories")
    return [Category(**cat) for cat in res]

async def get_category_by_id(category_id):
    res = await db.fetchrow(f"SELECT * FROM categories WHERE id={category_id}")
    if res:
        return Category(**res)
    return None

async def create_category(name) -> Category:
    try:
        await db.execute("INSERT INTO categories (name) VALUES ($1)", name)
    except Exception as e:
        print(e)
        return None
    cat = await db.fetchrow("SELECT * FROM categories WHERE name = $1", name)
    return Category(**cat)