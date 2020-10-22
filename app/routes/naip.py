"""NAIP endpoint."""

from titiler.custom.routing import apiroute_factory
from titiler.endpoints.factory import MosaicTilerFactory

from ..dependencies import MosaicParams

from fastapi import APIRouter

route_class = apiroute_factory(
    {
        # IMPORTANT NAIP is stored in a REQUESTER-PAYS bucket
        "AWS_REQUEST_PAYER": "requester",
        "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
        "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".tif",
    }
)

mosaicjson = MosaicTilerFactory(  # type: ignore
    path_dependency=MosaicParams,
    add_update=False,
    add_create=False,
    router=APIRouter(route_class=route_class),
    router_prefix="mosaicjson/naip",
)
