"""NAIP endpoint."""

from titiler.custom.routing import apiroute_factory
from titiler.endpoints.factory import MosaicTilerFactory

from ..dependencies import MosaicParams

from fastapi import APIRouter

route_class = apiroute_factory(
    {
        # IMPORTANT NAIP is stored in a REQUESTER-PAYS bucket
        "AWS_REQUEST_PAYER": "requester",
    }
)

mosaicjson = MosaicTilerFactory(  # type: ignore
    path_dependency=MosaicParams,
    # By default we do not use this API to create or store the mosaics
    add_update=False,
    add_create=False,
    router_prefix="mosaicjson/naip",
    router=APIRouter(route_class=route_class),
)
