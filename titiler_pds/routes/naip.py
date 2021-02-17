"""NAIP endpoint."""

from titiler.custom.routing import apiroute_factory
from titiler.endpoints.factory import MosaicTilerFactory
from titiler.resources.enums import OptionalHeaders

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
    optional_headers=[OptionalHeaders.server_timing, OptionalHeaders.x_assets],
)
