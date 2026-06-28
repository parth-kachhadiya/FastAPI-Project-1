
"""
FastAPI endpoint   : http://localhost:8000/

FastAPI metrics    : http://localhost:8000/metrics

Streamlit frontend : http://localhost:8501

Prometheus UI      : http://localhost:9090/
    Run query : http_requests_total

Grafana            : http://localhost:3000
    Username : admin
    Password : admin
"""

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

