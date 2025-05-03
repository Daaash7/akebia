from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Form
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.admin.models import Admin
from app.cart.accessor import get_all_cart, del_all_cart
from app.order.accessor import add_new_order, set_order_status, get_all_orders_admin
from app.order.models import Order
from app.user.models import User
from app.utils.cookies_session import get_current_user, get_current_admin
from app.utils.utils import templates
from app.warehouse.accessor import add_new_sale

router = APIRouter(
    prefix="/order",
)

class CreateOrder(BaseModel):
    address: str

class ChangeStatus(BaseModel):
    order_id: int
    status_id: int


@router.post("/create")
async def create_order_post(request: Request, address: Annotated[str, Form()], user: User = Depends(get_current_user)) -> Order:
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    cart = await get_all_cart(user.id)
    count = 0
    for item in cart:
        if item.count > 0:
            count += 1
    if count == 0:
        return RedirectResponse("/user", status_code=303)


    print("123")
    order_id = await add_new_order(user.id, address)
    print("1234")
    cart = await get_all_cart(user.id)
    print("12345")
    for product in cart:
        try:
            await add_new_sale(product.product.id, order_id)
        except Exception as e:
            print(e)
            continue
    print("1234567")
    await del_all_cart(user.id)
    return RedirectResponse("/user", status_code=303)

@router.get("/all")
async def all_orders(request: Request, admin: Admin = Depends(get_current_admin)):
    return templates.TemplateResponse("all_orders.html",
                                      {"request": request,
                                       "admin": admin,
                                       "orders": await get_all_orders_admin()
                                       })


@router.patch("/change_status")
async def change_status(request: ChangeStatus, admin: Admin = Depends(get_current_admin)):
    try:
        await set_order_status(request.order_id, request.status_id)
        return {'ok':True}
    except Exception as e:
        print(e)
        return {'ok':False}
