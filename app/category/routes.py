
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.requests import Request

from app.category.accessor import get_category_by_id, create_category
from app.manufacturers.accessor import get_manufacturer_by_id
from app.price.accessor import get_current_price
from app.products.accessor import get_products_by_category
from app.products.models import ProductCard
from app.utils.cookies_session import get_current_admin, get_current_user
from app.utils.utils import templates

router = APIRouter(
    prefix="/category",
)

class CategoryCreate(BaseModel):
    category_name: str

@router.get("")
async def category_by_id(request: Request, cat_id:int, user = Depends(get_current_user)):
    category = await get_category_by_id(cat_id)
    if not category:
        raise HTTPException(status_code=404)
    products = await get_products_by_category(cat_id)
    data = []
    for product_el in products:
        price = await get_current_price(product_el.id)
        manufacturer = await get_manufacturer_by_id(product_el.manufacturer_id)
        category = await get_category_by_id(product_el.category_id)
        data.append(
            ProductCard(
                product_el,
                price,
                manufacturer,
                category
            )
        )
    return templates.TemplateResponse("products_by_category.html",
                                      {"request": request,
                                       "cat_id": cat_id,
                                        "cards": data,
                                       "category": category,
                                       "current_user": user
                                       })

@router.get("/create")
async def create_category_template(request:Request, admin = Depends(get_current_admin)):
    return templates.TemplateResponse("create_category.html", {"request": request})

@router.post("/create")
async def create_category_api(request:Request, category_name: CategoryCreate, admin = Depends(get_current_admin)):
    res = await create_category(category_name.category_name)
    if not res:
        return {'ok': False}
    return {
        'ok': True,
        'category': res.name
    }

