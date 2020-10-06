"""Landsat endpoint."""

from dataclasses import dataclass, field
from typing import Dict, Type

from rio_tiler_pds.landsat.aws import L8Reader

from titiler.custom.routing import apiroute_factory
from titiler.dependencies import DefaultDependency
from titiler.endpoints.factory import TilerFactory, MosaicTilerFactory
from titiler.models.dataset import Info, Metadata

from ..dependencies import BandsExprParams, BandsParams, CustomPathParams

from fastapi import APIRouter, Depends

route_class = apiroute_factory(
    {
        "GDAL_DISABLE_READDIR_ON_OPEN": "FALSE",
        "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".TIF,.ovr",
    }
)


@dataclass
class LandsatTiler(TilerFactory):
    """Custom Tiler Class for STAC."""

    reader: Type[L8Reader] = field(default=L8Reader)

    path_dependency: Type[CustomPathParams] = CustomPathParams

    layer_dependency: Type[DefaultDependency] = BandsExprParams

    def info(self):
        """Register /info endpoint."""

        @self.router.get(
            "/info",
            response_model=Info,
            response_model_exclude={"minzoom", "maxzoom", "center"},
            response_model_exclude_none=True,
            responses={200: {"description": "Return dataset's basic info."}},
        )
        def info(
            src_path=Depends(self.path_dependency),
            bands=Depends(BandsParams),
            kwargs: Dict = Depends(self.additional_dependency),
        ):
            """Return basic info."""
            with self.reader(src_path.url, **self.reader_options) as src_dst:
                info = src_dst.info(bands=bands, **kwargs)
            return info

    def metadata(self):
        """Register /metadata endpoint."""

        @self.router.get(
            "/metadata",
            response_model=Metadata,
            response_model_exclude={"minzoom", "maxzoom", "center"},
            response_model_exclude_none=True,
            responses={200: {"description": "Return dataset's metadata."}},
        )
        def metadata(
            src_path=Depends(self.path_dependency),
            bands=Depends(BandsParams),
            metadata_params=Depends(self.metadata_dependency),
            kwargs: Dict = Depends(self.additional_dependency),
        ):
            """Return metadata."""
            with self.reader(src_path.url, **self.reader_options) as src_dst:
                info = src_dst.metadata(
                    metadata_params.pmin,
                    metadata_params.pmax,
                    bands=bands,
                    **metadata_params.kwargs,
                    **kwargs,
                )
            return info


scenes = LandsatTiler(  # type: ignore
    router=APIRouter(route_class=route_class),
    router_prefix="scenes/landsat"
)

mosaicjson = MosaicTilerFactory(  # type: ignore
    dataset_reader=L8Reader,
    layer_dependency=BandsExprParams,
    add_update=False,
    add_create=False,
    router=APIRouter(route_class=route_class),
    router_prefix="mosaicjson/landsat",
)
