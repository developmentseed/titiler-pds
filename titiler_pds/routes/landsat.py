"""Landsat endpoint."""

from rio_tiler_pds.landsat.aws import L8Reader

from titiler.custom.routing import apiroute_factory
from titiler.dependencies import BandsExprParams
from titiler.endpoints.factory import MosaicTilerFactory, MultiBandTilerFactory

from ..dependencies import CustomPathParams, MosaicParams

from fastapi import APIRouter

route_class = apiroute_factory(
    {
        "AWS_NO_SIGN_REQUEST": "YES",
        "GDAL_DISABLE_READDIR_ON_OPEN": "FALSE",
        "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".TIF,.ovr",
    }
)

scenes = MultiBandTilerFactory(
    reader=L8Reader,
    path_dependency=CustomPathParams,
    router_prefix="scenes/landsat",
    router=APIRouter(route_class=route_class),
)

mosaicjson = MosaicTilerFactory(
    path_dependency=MosaicParams,
    dataset_reader=L8Reader,
    layer_dependency=BandsExprParams,
    router_prefix="mosaicjson/landsat",
    router=APIRouter(route_class=route_class),
)
