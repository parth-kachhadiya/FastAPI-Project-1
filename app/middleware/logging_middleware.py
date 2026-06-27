import logging
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req, next):
        logging.info(f"Request : Method : {req.method} | endpoint : {req.url}")
        response = await next(req)
        logging.info(f"Response : Status code : {response.status_code}")
        return response