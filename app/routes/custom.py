"""Custom endpoint."""

from dataclasses import dataclass
from typing import Dict

from titiler.endpoints.factory import TilerFactory
from titiler.models.dataset import Info, Metadata

from ..dependencies import BandsParams

from fastapi import Depends


@dataclass
class SceneTiler(TilerFactory):
    """Custom Tiler Class for STAC."""

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
