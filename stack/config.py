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

    # Default PDS buckets
    buckets: List = ["landsat-pds", "sentinel-cogs", "naip-visualization"]

    timeout: int = 30
    memory: int = 3009

    # The maximum of concurrent executions you want to reserve for the function.
    # Default: - No specific limit - account limit.
    max_concurrent: Optional[int]

    # mosaic
    mosaic_backend: str
    mosaic_host: str
    # format will be ignored for dynamodb backend
    mosaic_format: str = ".json.gz"

    class Config:
        """model config"""

        env_file = "stack/.env"
        env_prefix = "STACK_"
