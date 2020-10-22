"""Sentinel endpoint."""

from rio_tiler_pds.sentinel.aws import S2COGReader

from titiler.custom.routing import apiroute_factory
from titiler.endpoints.factory import MosaicTilerFactory

from ..dependencies import BandsExprParams, CustomPathParams, MosaicParams
from .custom import SceneTiler

from fastapi import APIRouter

route_class = apiroute_factory(
    {
        "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
        "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".tif",
    }
)

scenes = SceneTiler(  # type: ignore
    reader=S2COGReader,
    path_dependency=CustomPathParams,
    layer_dependency=BandsExprParams,
    router=APIRouter(route_class=route_class),
    router_prefix="scenes/sentinel",
)

mosaicjson = MosaicTilerFactory(  # type: ignore
    path_dependency=MosaicParams,
    dataset_reader=S2COGReader,
    layer_dependency=BandsExprParams,
    add_update=False,
    add_create=False,
    router=APIRouter(route_class=route_class),
    router_prefix="mosaicjson/sentinel",
)
