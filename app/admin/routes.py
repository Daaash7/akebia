import json
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Body
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from app.admin.accessor import validate_admin
from app.category.accessor import get_all_categories
from app.manufacturers.accessor import get_all_manufacturers
from app.utils.cookies_session import get_current_admin, COOKIE_NAME, get_admin_token
from app.utils.utils import templates

router = APIRouter(
    prefix="/admin"
)

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request, "title": "Главная"})

@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, response: Response, username: Annotated[str, Body()], password: Annotated[str, Body()]):
    admin = await validate_admin(username, password)
    if admin:
        token = get_admin_token(response, admin.id)
        response.set_cookie(key = COOKIE_NAME, value = str(token))
    else:
        raise HTTPException(status_code=403)
    return json.dumps({'ok': True})

@router.get("/getme", response_class=HTMLResponse)
async def getme(request: Request, admin = Depends(get_current_admin)):
    return json.dumps({
        'ok':True,
        'admin':{
            'name':admin.name,
        }
    })

@router.get("", response_class=HTMLResponse)
async def index(request: Request, admin = Depends(get_current_admin)):
    return templates.TemplateResponse("admin_panel.html",
                                      {"request": request,
                                       "admin":admin,
                                       "categories": await get_all_categories(),
                                       "manufacturers": await get_all_manufacturers()
                                       })