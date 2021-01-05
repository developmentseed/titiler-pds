"""Landsat endpoint."""

from rio_tiler_pds.landsat.aws import L8Reader

from titiler.endpoints.factory import MosaicTilerFactory

from ..dependencies import BandsExprParams, CustomPathParams, MosaicParams
from .custom import SceneTiler

config = {
    "GDAL_DISABLE_READDIR_ON_OPEN": "FALSE",
    "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".TIF,.ovr",
}

scenes = SceneTiler(  # type: ignore
    reader=L8Reader,
    path_dependency=CustomPathParams,
    layer_dependency=BandsExprParams,
    router_prefix="scenes/landsat",
    gdal_config=config,
)

mosaicjson = MosaicTilerFactory(  # type: ignore
    path_dependency=MosaicParams,
    dataset_reader=L8Reader,
    layer_dependency=BandsExprParams,
    add_update=False,
    add_create=False,
    router_prefix="mosaicjson/landsat",
    gdal_config=config,
)
