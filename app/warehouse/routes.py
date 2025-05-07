from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

from app.admin.models import Admin
from app.utils.cookies_session import get_current_admin
from app.warehouse.accessor import add_deliver

router = APIRouter(
    prefix="/warehouse",
)

class AddWarehouse(BaseModel):
    product_id: int
    count: int

@router.post("/add")
async def add_deliver_product(request: AddWarehouse, admin: Admin = Depends(get_current_admin)):
    res = await add_deliver(request.product_id, request.count)
    if res:
        return {'ok': True}
    return HTTPException(status_code=401)