from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

from app.admin.models import Admin
from app.price.accessor import set_price
from app.utils.cookies_session import get_current_admin

router = APIRouter(
    prefix="/price",
)

class SetPrice(BaseModel):
    product_id: int
    price: int

@router.post("/set")
async def set_price_post(request: SetPrice, admin: Admin = Depends(get_current_admin)):
    try:
        await set_price(product_id=request.product_id, price=request.price)
        return {'ok':True}
    except Exception:
        return HTTPException(status_code=400, detail='Something went wrong')