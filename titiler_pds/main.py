"""titiler-pds app."""

import logging

from brotli_asgi import BrotliMiddleware
from tilebench.middleware import VSIStatsMiddleware

from titiler.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from titiler.middleware import CacheControlMiddleware, TotalTimeMiddleware

from .routes import landsat_collection2, naip, sentinel
from .settings import api_config

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

# turn off or quiet logs
logging.getLogger("botocore.credentials").disabled = True
logging.getLogger("botocore.utils").disabled = True
logging.getLogger("rio-tiler").setLevel(logging.ERROR)

app = FastAPI(title="titiler-pds", version="0.1.0")

add_exception_handlers(app, DEFAULT_STATUS_CODES)
if api_config.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_config.cors_origins,
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

app.add_middleware(BrotliMiddleware, minimum_size=0, gzip_fallback=True)
app.add_middleware(CacheControlMiddleware, cachecontrol=api_config.cachecontrol)

if api_config.debug:
    app.add_middleware(TotalTimeMiddleware)

if api_config.vsi_stats:
    app.add_middleware(VSIStatsMiddleware)

app.include_router(
    landsat_collection2.scenes.router, prefix="/scenes/landsat", tags=["Landsat"]
)
app.include_router(
    landsat_collection2.mosaicjson.router,
    prefix="/mosaicjson/landsat",
    tags=["Landsat"],
)

app.include_router(
    sentinel.scenes.router, prefix="/scenes/sentinel", tags=["Sentinel 2 COG"]
)
app.include_router(
    sentinel.mosaicjson.router, prefix="/mosaicjson/sentinel", tags=["Sentinel 2 COG"]
)

# NAIP tiler is a regular tiler with requester-pays set
app.include_router(naip.mosaicjson.router, prefix="/mosaicjson/naip", tags=["NAIP"])


@app.get("/healtz", description="Health Check", tags=["Health Check"])
def ping():
    """Health check."""
    return {"ping": "pong!"}
