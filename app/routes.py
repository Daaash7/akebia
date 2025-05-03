from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.admin.routes import router as admin_router
from app.user.routes import router as user_router
from app.main_page.routes import router as main_page_router
from app.category.routes import router as category_router
from app.manufacturers.routes import router as manufacturer_router
from app.products.routes import router as products_router
from app.cart.routes import router as cart_router
from app.order.routes import router as order_router


def setup_routes(app: FastAPI):
    app.mount("/static", StaticFiles(directory="../static"), name="static")

    app.include_router(admin_router)

    app.include_router(user_router)
    app.include_router(main_page_router)
    app.include_router(category_router)
    app.include_router(manufacturer_router)
    app.include_router(products_router)
    app.include_router(cart_router)
    app.include_router(order_router)