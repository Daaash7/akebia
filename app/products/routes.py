from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.params import Depends, Query
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.cart.accessor import add_to_cart, check_product_in_cart, del_from_cart
from app.category.accessor import get_all_categories, get_category_by_id
from app.manufacturers.accessor import get_all_manufacturers, get_manufacturer_by_id
from app.price.accessor import get_current_price
from app.products.accessor import create_product, get_product_by_id, add_product_to_new_coll, del_product_from_new_coll
from app.user.models import User
from app.utils.cookies_session import get_current_admin, get_current_user
from app.utils.utils import templates, save_product_image
from app.warehouse.accessor import get_product_count

router = APIRouter(
    prefix="/product",
)

class AddToCart(BaseModel):
    product_id: int

@router.get("/create")
async def create_product_get(request: Request, admin = Depends(get_current_admin)):
    return templates.TemplateResponse("create_product.html",
                                      {"request": request,
                                       "manufacturers": await get_all_manufacturers(),
                                       "categories": await get_all_categories()})

@router.post("/create")
async def create_product_post(request: Request,
                         product_name: Annotated[str, Form()],
                         product_description: Annotated[str, Form()],
                         category_id: Annotated[int, Form()],
                         product_image: Annotated[UploadFile, File()],
                        product_price: Annotated[int, Form()],
                        is_new_collection: Annotated[bool, Form()],
                         admin = Depends(get_current_admin)
                              ):
    image_filename = save_product_image(product_name, product_image)
    try:
        data = await create_product(product_name, product_description, category_id, image_filename, product_price)
        if is_new_collection:
            await add_product_to_new_coll(data.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if data:
        return RedirectResponse(url=f"/product?pr_id={data.id}", status_code=303)
    else:
        raise HTTPException(status_code=409, detail="Error")

@router.get("/")
async def product_get(request: Request, pr_id: Annotated[int, Query()], user: User = Depends(get_current_user)):
    product = await get_product_by_id(pr_id)
    is_in_cart = False
    if user:
        is_in_cart = await check_product_in_cart(product.id, user.id)
    if not product:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("product.html",
                                      {"request": request,
                                       "product": product,
                                       "category": await get_category_by_id(product.category_id),
                                       "price": await get_current_price(product.id),
                                       "count": await get_product_count(product.id),
                                       "is_in_cart": is_in_cart,
                                       "current_user": await get_current_user(request),
                                       "page_name": product.name,
                                       })

@router.post("/add_to_cart")
async def add_to_cart_post(request: AddToCart, user: User = Depends(get_current_user)):
    if not user:
        return HTTPException(status_code=401, detail="Not Authorized")
    product_id = request.product_id
    product = await get_product_by_id(int(product_id))
    print(product)
    if not product:
        raise HTTPException(status_code=404)
    res = await add_to_cart(user.id, product_id, 1)
    if not res:
        raise HTTPException(status_code=409)
    else:
        return {'ok': True}

@router.delete("/del_from_cart")
async def delete_from_cart_del(request: Request, pr_id = Annotated[int, Query()], user: User = Depends(get_current_user)):
    if not user:
        return HTTPException(status_code=401, detail="Not Authorized")
    try:
        await del_from_cart(user.id, int(pr_id))
        return {'ok': True}
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.post("/add_to_new_collection")
async def add_to_new_collection(request: AddToCart, admin = Depends(get_current_admin)):
    if await add_product_to_new_coll(request.product_id):
        return {'ok': True}
    return HTTPException(status_code=409, detail="Error")

@router.delete("/del_to_new_collection")
async def add_to_new_collection(request: AddToCart, admin = Depends(get_current_admin)):
    if await del_product_from_new_coll(request.product_id):
        return {'ok': True}
    return HTTPException(status_code=409, detail="Error")