"""app dependencies."""

import re
from dataclasses import dataclass, field
from typing import Dict, Optional, Sequence

from rio_tiler_pds.landsat.utils import sceneid_parser as l8_sceneid_parser
from rio_tiler_pds.sentinel.utils import s2_sceneid_parser

from titiler.dependencies import DefaultDependency

from .settings import mosaic_config

from fastapi import HTTPException, Query


@dataclass
class CustomPathParams:
    """Create dataset path from args"""

    sceneid: str = Query(..., description="Sceneid.")
    scene_metadata: Dict = field(init=False)

    def __post_init__(self,):
        """Define dataset URL."""
        self.url = self.sceneid
        if self.sceneid.startswith("S2"):
            self.scene_metadata = s2_sceneid_parser(self.sceneid)
        elif self.sceneid.startswith("L8"):
            self.scene_metadata = l8_sceneid_parser(self.sceneid)


def BandsParams(
    bands: str = Query(
        ..., title="bands names", description="comma (',') delimited bands names.",
    )
) -> Sequence[str]:
    """Bands."""
    return bands.split(",")


@dataclass
class BandsExprParams(DefaultDependency):
    """Band names and Expression parameters."""

    bands: Optional[str] = Query(
        None, title="bands names", description="comma (',') delimited bands names.",
    )
    expression: Optional[str] = Query(
        None,
        title="Band Math expression",
        description="rio-tiler's band math expression.",
    )

    def __post_init__(self):
        """Post Init."""
        if self.bands is not None:
            self.kwargs["bands"] = self.bands.split(",")
        if self.expression is not None:
            self.kwargs["expression"] = self.expression


@dataclass
class MosaicParams:
    """Create mosaic path from args"""

    layer: str = Query(..., description="Mosaic Layer name ('{username}.{layer}')")

    def __post_init__(self,):
        """Define mosaic URL."""
        pattern = (
            r"^(?P<username>[a-zA-Z0-9-_]{1,32})\.(?P<layername>[a-zA-Z0-9-_]{1,32})$"
        )
        if not re.match(pattern, self.layer):
            raise HTTPException(
                status_code=400, detail=f"Invalid layer name: `{self.layer}`",
            )
        if mosaic_config.backend == "dynamodb://":
            self.url = f"{mosaic_config.backend}{mosaic_config.host}:{self.layer}"
        else:
            self.url = f"{mosaic_config.backend}{mosaic_config.host}/{self.layer}{mosaic_config.format}"
