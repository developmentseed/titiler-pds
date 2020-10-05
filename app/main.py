"""titiler-pds app."""

from mangum import Mangum

from titiler.errors import DEFAULT_STATUS_CODES, add_exception_handlers

from .routes import landsat, sentinel

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request

app = FastAPI(title="titiler-pds", version="0.1.0")
app.include_router(landsat.router, prefix="/landsat", tags=["Landsat 8"])
app.include_router(sentinel.router, prefix="/sentinel", tags=["Sentinel 2 COG"])
add_exception_handlers(app, DEFAULT_STATUS_CODES)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=0)


@app.middleware("http")
async def header_middleware(request: Request, call_next):
    """Add custom header."""
    response = await call_next(request)
    if (
        not response.headers.get("Cache-Control")
        and request.method in ["HEAD", "GET"]
        and response.status_code < 500
    ):
        response.headers["Cache-Control"] = "public, max-age=3600"
    return response


@app.get("/ping", description="Health Check", tags=["Health Check"])
def ping():
    """Health check."""
    return {"ping": "pong!"}


handler = Mangum(app, log_level="error")
