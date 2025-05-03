
from app.admin.models import Admin
from app.store.database import db
from app.utils.utils import get_hash


async def validate_admin(name, password) -> Admin | None:
    data = await db.fetchrow("""SELECT * FROM admins WHERE name=$1 and password=$2""", name, get_hash(password))
    if data:
        return Admin(**data)
    return None


async def get_admin_by_id(id) -> Admin | None:
    data = await db.fetchrow("""SELECT * FROM admins WHERE id=$1""", (id))
    if data:
        return Admin(**data)
    return None

async def create_admin(email, password):
    await db.execute("INSERT INTO admins (email, password) VALUES (?, ?)", (email, get_hash(password)))
