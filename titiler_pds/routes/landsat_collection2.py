"""Landsat endpoint."""

from rio_tiler_pds.landsat.aws import LandsatC2Reader

from titiler.custom.routing import apiroute_factory
from titiler.endpoints.factory import MosaicTilerFactory

from ..dependencies import BandsExprParams, CustomPathParams, MosaicParams
from .custom import SceneTiler

from fastapi import APIRouter

route_class = apiroute_factory(
    {
        # IMPORTANT Landsat collection 2 is stored in a REQUESTER-PAYS bucket
        "AWS_REQUEST_PAYER": "requester",
    }
)

scenes = SceneTiler(  # type: ignore
    reader=LandsatC2Reader,
    path_dependency=CustomPathParams,
    layer_dependency=BandsExprParams,
    router_prefix="scenes/landsat",
    router=APIRouter(route_class=route_class),
)

mosaicjson = MosaicTilerFactory(  # type: ignore
    path_dependency=MosaicParams,
    dataset_reader=LandsatC2Reader,
    layer_dependency=BandsExprParams,
    # By default we do not use this API to create or store the mosaics
    add_update=False,
    add_create=False,
    router_prefix="mosaicjson/landsat",
    router=APIRouter(route_class=route_class),
)
