from fastapi import FastAPI

from app.admin.middlewares import AdminAuthMiddleware

def setup_middlewares(app: FastAPI):
    app.add_middleware(AdminAuthMiddleware)