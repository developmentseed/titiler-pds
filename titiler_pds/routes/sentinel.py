"""Sentinel endpoint."""

from rio_tiler_pds.sentinel.aws import S2COGReader

from titiler.custom.routing import apiroute_factory
from titiler.dependencies import BandsExprParams
from titiler.endpoints.factory import MosaicTilerFactory, MultiBandTilerFactory

from ..dependencies import CustomPathParams, MosaicParams

from fastapi import APIRouter

route_class = apiroute_factory({"AWS_NO_SIGN_REQUEST": "YES"})


scenes = MultiBandTilerFactory(
    reader=S2COGReader,
    path_dependency=CustomPathParams,
    router_prefix="scenes/sentinel",
    router=APIRouter(route_class=route_class),
)

mosaicjson = MosaicTilerFactory(
    path_dependency=MosaicParams,
    dataset_reader=S2COGReader,
    layer_dependency=BandsExprParams,
    router_prefix="mosaicjson/sentinel",
    router=APIRouter(route_class=route_class),
)
