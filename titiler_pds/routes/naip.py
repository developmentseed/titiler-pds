"""NAIP endpoint."""

from titiler.core.resources.enums import OptionalHeader
from titiler.core.routing import apiroute_factory
from titiler.mosaic.factory import MosaicTilerFactory

from ..dependencies import MosaicParams

from fastapi import APIRouter

route_class = apiroute_factory(
    {
        # IMPORTANT NAIP is stored in a REQUESTER-PAYS bucket
        "AWS_DEFAULT_REGION": "us-west-2",
        "AWS_REQUEST_PAYER": "requester",
    }
)

mosaicjson = MosaicTilerFactory(  # type: ignore
    path_dependency=MosaicParams,
    router_prefix="mosaicjson/naip",
    router=APIRouter(route_class=route_class),
    optional_headers=[OptionalHeader.server_timing, OptionalHeader.x_assets],
)
