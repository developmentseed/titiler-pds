"""app settings"""

from typing import Optional

import pydantic


class MosaicSettings(pydantic.BaseSettings):
    """Application settings"""

    backend: str
    host: str
    format: Optional[str]

    class Config:
        """model config"""

        env_prefix = "MOSAIC_"


mosaic_config = MosaicSettings()
