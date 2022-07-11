"""Sentinel endpoint."""

from rio_tiler_pds.sentinel.aws import S2COGReader

from titiler.core.dependencies import BandsExprParams
from titiler.core.factory import MultiBandTilerFactory
from titiler.core.routing import apiroute_factory
from titiler.mosaic.factory import MosaicTilerFactory

from ..dependencies import CustomPathParams, MosaicParams

from fastapi import APIRouter, Depends


def get_callable_dependency(value: CustomPathParams = Depends(callable_dependency)):
    return value.sceneid


route_class = apiroute_factory({"AWS_NO_SIGN_REQUEST": "YES"})

scenes = MultiBandTilerFactory(
    reader=S2COGReader,
    path_dependency=get_callable_dependency,
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
