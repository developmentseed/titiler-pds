"""STACK Configs."""

from typing import Dict, List, Optional

import pydantic


class StackSettings(pydantic.BaseSettings):
    """Application settings"""

    name: str = "titiler-pds"
    stage: str = "production"

    owner: Optional[str]
    client: Optional[str]
    project: Optional[str]

    additional_env: Dict = {}

    buckets: List = ["landsat-pds", "sentinel-cogs"]

    timeout: int = 30
    memory: int = 3008

    # The maximum of concurrent executions you want to reserve for the function.
    # Default: - No specific limit - account limit.
    max_concurrent: Optional[int]

    # mosaic
    mosaic_backend: str
    mosaic_host: str
    mosaic_format: Optional[str]

    class Config:
        """model config"""

        env_file = "stack/.env"
        env_prefix = "STACK_"


stack_config = StackSettings()
