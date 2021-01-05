"""Custom endpoint."""

from dataclasses import dataclass
from typing import Dict

import rasterio
from geojson_pydantic.features import Feature
from rio_tiler.models import Info, Metadata

from titiler.endpoints.factory import TilerFactory
from titiler.ressources.responses import GeoJSONResponse
from titiler.utils import bbox_to_feature

from ..dependencies import BandsParams

from fastapi import Depends


@dataclass
class SceneTiler(TilerFactory):
    """Custom Tiler Class."""

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
            with rasterio.Env(**self.gdal_config):
                with self.reader(src_path.url, **self.reader_options) as src_dst:
                    return src_dst.info(bands=bands, **kwargs)

        @self.router.get(
            "/info.geojson",
            response_model=Feature,
            response_model_exclude_none=True,
            response_class=GeoJSONResponse,
            responses={
                200: {
                    "content": {"application/geo+json": {}},
                    "description": "Return dataset's basic info as a GeoJSON feature.",
                }
            },
        )
        def info_geojson(
            src_path=Depends(self.path_dependency),
            bands=Depends(BandsParams),
            kwargs: Dict = Depends(self.additional_dependency),
        ):
            """Return dataset's basic info as a GeoJSON feature."""
            with rasterio.Env(**self.gdal_config):
                with self.reader(src_path.url, **self.reader_options) as src_dst:
                    info = {"scene": src_path.url}
                    info["bands"] = {
                        band: meta.dict(exclude_none=True)
                        for band, meta in src_dst.info(bands=bands, **kwargs).items()
                    }
                    return bbox_to_feature(src_dst.bounds, properties=info)

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
            with rasterio.Env(**self.gdal_config):
                with self.reader(src_path.url, **self.reader_options) as src_dst:
                    return src_dst.metadata(
                        metadata_params.pmin,
                        metadata_params.pmax,
                        bands=bands,
                        **metadata_params.kwargs,
                        **kwargs,
                    )
