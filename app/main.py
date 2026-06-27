from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import route_auth, route_predict
from app.middleware.logging_middleware import LoggingMiddleware
from app.core.exceptions import registerExceptionHandlers

app = FastAPI(title = "Car Price Prediction API")

# Middleware link
app.add_middleware(LoggingMiddleware)

# Route link
app.include_router(route_auth.router, tags=['Auth Route'])
app.include_router(route_predict.router, tags=['Prediction Route'])

# Monitoring using prometheus 
Instrumentator().instrument(app).expose(app)

# Add exception handler
registerExceptionHandlers(app)