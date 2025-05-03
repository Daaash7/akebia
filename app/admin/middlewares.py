from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.utils.cookies_session import get_current_admin


class AdminAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Dictionary to store request counts for each IP
        self.request_counts = {}

    async def dispatch(self, request: Request, call_next):
        admin_pages = ["/admin", "/product/create", "/manufacturer/create", "/category/create", "/order/all"]
        res = await call_next(request)
        if request.url.path in admin_pages:
            try:
                await get_current_admin(request)
                return res
            except Exception:
                return RedirectResponse("/admin/login")
        return res

