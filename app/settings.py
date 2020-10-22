"""app settings"""

import pydantic


class MosaicSettings(pydantic.BaseSettings):
    """Application settings"""

    backend: str
    host: str
    # format will be ignored for dynamodb backend
    format: str = ".json.gz"

    class Config:
        """model config"""

        env_prefix = "MOSAIC_"


mosaic_config = MosaicSettings()
