from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.middlewares import setup_middlewares
from app.routes import setup_routes
from app.store.database import lifespan

app = FastAPI(lifespan=lifespan)

setup_routes(app)
setup_middlewares(app)

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     print("asd")
#     if request.method == "GET":
#         return templates.TemplateResponse("error_page.html",
#                                           {"request": request,
#                                            "code": exc.status_code,
#                                            "message": exc.detail
#                                            })
#     # return JSONResponse(exc.detail, status_code=exc.status_code)

app.mount("/static", StaticFiles(directory="static"), name="static")