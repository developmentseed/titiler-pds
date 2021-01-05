"""Sentinel endpoint."""

from rio_tiler_pds.sentinel.aws import S2COGReader

from titiler.endpoints.factory import MosaicTilerFactory

from ..dependencies import BandsExprParams, CustomPathParams, MosaicParams
from .custom import SceneTiler

scenes = SceneTiler(  # type: ignore
    reader=S2COGReader,
    path_dependency=CustomPathParams,
    layer_dependency=BandsExprParams,
    router_prefix="scenes/sentinel",
)

mosaicjson = MosaicTilerFactory(  # type: ignore
    path_dependency=MosaicParams,
    dataset_reader=S2COGReader,
    layer_dependency=BandsExprParams,
    add_update=False,
    add_create=False,
    router_prefix="mosaicjson/sentinel",
)
