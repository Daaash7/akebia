from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.cart.accessor import get_all_cart
from app.user.models import User
from app.utils.cookies_session import get_current_user
from app.utils.utils import templates

router = APIRouter(
    prefix="/cart",
)

@router.get("/")
async def get_cart_get(request: Request, user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse("/user/login")
    return templates.TemplateResponse("cart.html",
                                      {"request": request,
                                       "current_user": user,
                                       "cart": await get_all_cart(user.id)
                                       })