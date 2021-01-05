"""NAIP endpoint."""

from titiler.endpoints.factory import MosaicTilerFactory

from ..dependencies import MosaicParams

# IMPORTANT NAIP is stored in a REQUESTER-PAYS bucket
config = {"AWS_REQUEST_PAYER": "requester"}

mosaicjson = MosaicTilerFactory(  # type: ignore
    path_dependency=MosaicParams,
    add_update=False,
    add_create=False,
    router_prefix="mosaicjson/naip",
    gdal_config=config,
)
