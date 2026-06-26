from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def registerExceptionHandlers(app : FastAPI):
    @app.add_exception_handler(Exception)
    async def unhandledException(req : Request, e : Exception):
        return JSONResponse(
            status_code = 500,
            content = {
                'detail' : str(e)
            }
        )