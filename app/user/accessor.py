from app.store.database import db
from app.user.models import User
from app.utils.utils import get_hash


async def create_user(username: str, phone_number: str, password: str) -> User | None:
    try:
        await db.execute("INSERT INTO users (username, phone_number, password) VALUES ($1, $2, $3);", username, phone_number, get_hash(password))
        user = await db.fetchrow("SELECT * FROM users WHERE username = $1", username)
        return User(**user)

    except Exception as e:
        return None

async def get_user_by_id(id: int) -> User | None:
    data = await db.fetchrow("""SELECT * FROM users WHERE id=$1""", (id))
    if data:
        return User(**data)
    return None

async def validate_user(username: str, password: str) -> User | None:
    data = await db.fetchrow("""SELECT * FROM users WHERE username=$1 and password=$2""", username, get_hash(password))
    if data:
        return User(**data)
    return None
