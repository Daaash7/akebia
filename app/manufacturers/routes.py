from typing import Annotated

from fastapi import APIRouter, Form, File, UploadFile
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.category.accessor import get_category_by_id
from app.manufacturers.accessor import get_manufacturer_by_id, create_manufacturer
from app.price.accessor import get_current_price
from app.products.accessor import get_product_by_manufacturer
from app.products.models import ProductCard
from app.utils.cookies_session import get_current_admin, get_current_user
from app.utils.utils import templates, save_manufacturer_image

router = APIRouter(
    prefix="/manufacturer",
)

class ManufacturerCreate(BaseModel):
    manufacturer_name: str

@router.get("")
async def manufacturer_by_id(request: Request, man_id:int, user = Depends(get_current_user)):
    manufacturer = await get_manufacturer_by_id(man_id)
    if not manufacturer:
        raise HTTPException(status_code=404)
    products = await get_product_by_manufacturer(man_id)
    data = []
    for product_el in products:
        price = await get_current_price(product_el.id)
        manufacturer = await get_manufacturer_by_id(product_el.manufacturer_id)
        category = await get_category_by_id(product_el.category_id)
        data.append(
            ProductCard (
                product_el,
                price,
                manufacturer,
                category
            )
        )
    print(data)
    return templates.TemplateResponse("products_by_manufacturer.html",
                                      {"request": request,
                                       "man_id": man_id,
                                       "cards": data,
                                       "manufacturer": manufacturer,
                                       "current_user": user
                                       })


@router.get("/create")
async def create_manufacturer_template(request:Request, admin = Depends(get_current_admin)):
    return templates.TemplateResponse("create_manufacturer.html", {"request": request})

@router.post("/create")
async def create_manufacturer_api(request:Request, manufacturer_name: Annotated[str, Form()], manufacturer_image: Annotated[UploadFile, File()], admin = Depends(get_current_admin)):
    image_filename = save_manufacturer_image(manufacturer_name, manufacturer_image)
    res = await create_manufacturer(manufacturer_name, image_filename)
    if res:
        return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=409)


