from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Depends
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse

from app.cart.accessor import get_all_cart
from app.order.accessor import get_all_orders
from app.user.accessor import create_user, validate_user
from app.user.models import User
from app.utils.cookies_session import COOKIE_NAME, get_user_token, get_current_user
from app.utils.utils import templates

router = APIRouter(
    prefix="/user"
)

@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("user_registration.html", {"request": request, "title": "Главная"})

@router.post("/register")
async def register_post(request: Request, response: Response, username: Annotated[str, Body()], phone_number: Annotated[str, Body()], password: Annotated[str, Body()]):
    data = await create_user(username, phone_number, password)
    if data:
        token = get_user_token(response, data.id)
        response.delete_cookie(COOKIE_NAME)
        response.set_cookie(key = COOKIE_NAME, value = str(token))
        return {
            'ok':True,
            'user': {
                'username': data.username,
                'phone_number': data.phone_number,
            }
        }
    else:
        return HTTPException(status_code=409)

@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("user_login.html", {"request": request})

@router.post("/login")
async def login_post(request: Request, response: Response, username: Annotated[str, Body()], password: Annotated[str, Body()]):
    user = await validate_user(username, password)
    if user:
        token = get_user_token(response, user.id)
        response.delete_cookie(COOKIE_NAME)
        response.set_cookie(key=COOKIE_NAME, value=str(token))
        return {
            'ok':True,
            'user': {
                'username': user.username,
                'phone_number': user.phone_number,
            }
        }
    else:
        return {
            'ok': False,
        }

@router.get("")
async def user_page(request: Request, user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse('/user/login')
    print(await get_all_orders(user.id))
    return templates.TemplateResponse("user_page.html",
                                      {"request": request,
                                       "current_user": user,
                                       "cart": await get_all_cart(user.id),
                                       "orders": await get_all_orders(user.id)
                                       })


