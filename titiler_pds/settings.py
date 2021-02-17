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

        env_file = ".env"
        env_prefix = "MOSAIC_"


class ApiSettings(pydantic.BaseSettings):
    """FASTAPI application settings."""

    cors_origins: str = "*"
    cachecontrol: str = "public, max-age=3600"
    debug: bool = False
    vsi_stats: bool = False

    @pydantic.validator("cors_origins")
    def parse_cors_origin(cls, v):
        """Parse CORS origins."""
        return [origin.strip() for origin in v.split(",")]


mosaic_config = MosaicSettings()
api_config = ApiSettings()
