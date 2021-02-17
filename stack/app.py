"""Construct App."""

import os
from typing import Any, List, Optional

from aws_cdk import aws_apigatewayv2 as apigw
from aws_cdk import aws_apigatewayv2_integrations as apigw_integrations
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda, core
from config import StackSettings

settings = StackSettings()


DEFAULT_ENV = dict(
    CPL_TMPDIR="/tmp",
    GDAL_CACHEMAX="75%",
    CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
    GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
    GDAL_HTTP_MERGE_CONSECUTIVE_RANGES="YES",
    GDAL_HTTP_MULTIPLEX="YES",
    GDAL_HTTP_VERSION="2",
    PYTHONWARNINGS="ignore",
    VSI_CACHE="TRUE",
    VSI_CACHE_SIZE="1000000",
)


class LambdaStack(core.Stack):
    """Lambda Stack"""

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        memory: int = 1024,
        timeout: int = 30,
        runtime: aws_lambda.Runtime = aws_lambda.Runtime.PYTHON_3_8,
        concurrent: Optional[int] = None,
        permissions: Optional[List[iam.PolicyStatement]] = None,
        env: dict = {},
        code_dir: str = "./",
        **kwargs: Any,
    ) -> None:
        """Define stack."""
        super().__init__(scope, id, *kwargs)

        permissions = permissions or []

        lambda_env = {**DEFAULT_ENV, **env}
        lambda_env.update(
            dict(
                MOSAIC_BACKEND=settings.mosaic_backend,
                MOSAIC_HOST=settings.mosaic_host,
            )
        )

        lambda_function = aws_lambda.Function(
            self,
            f"{id}-lambda",
            runtime=runtime,
            code=aws_lambda.Code.from_asset(
                path=os.path.abspath(code_dir),
                bundling=core.BundlingOptions(
                    image=core.BundlingDockerImage.from_asset(
                        os.path.abspath(code_dir), file="Dockerfile",
                    ),
                    command=["bash", "-c", "cp -R /var/task/. /asset-output/."],
                ),
            ),
            handler="titiler_pds.handler.handler",
            memory_size=memory,
            reserved_concurrent_executions=concurrent,
            timeout=core.Duration.seconds(timeout),
            environment=lambda_env,
        )

        for perm in permissions:
            lambda_function.add_to_role_policy(perm)

        api = apigw.HttpApi(
            self,
            f"{id}-endpoint",
            default_integration=apigw_integrations.LambdaProxyIntegration(
                handler=lambda_function
            ),
        )
        core.CfnOutput(self, "Endpoint", value=api.url)


app = core.App()

perms = []
if settings.buckets:
    perms.append(
        iam.PolicyStatement(
            actions=["s3:GetObject", "s3:HeadObject"],
            resources=[f"arn:aws:s3:::{bucket}*" for bucket in settings.buckets],
        )
    )

stack = core.Stack()
if settings.mosaic_backend == "dynamodb://":
    perms.append(
        iam.PolicyStatement(
            actions=["dynamodb:GetItem", "dynamodb:Scan", "dynamodb:BatchWriteItem"],
            resources=[f"arn:aws:dynamodb:{stack.region}:{stack.account}:table/*"],
        )
    )

if settings.mosaic_backend == "s3://":
    perms.append(
        iam.PolicyStatement(
            actions=["s3:GetObject", "s3:HeadObject", "s3:PutObject"],
            resources=[f"arn:aws:s3:::{settings.mosaic_host}*"],
        )
    )

# Tag infrastructure
for key, value in {
    "Project": settings.name,
    "Stack": settings.stage,
    "Owner": settings.owner,
    "Client": settings.client,
}.items():
    if value:
        core.Tag.add(app, key, value)


LambdaStack(
    app,
    f"{settings.name}-{settings.stage}",
    memory=settings.memory,
    timeout=settings.timeout,
    concurrent=settings.max_concurrent,
    permissions=perms,
    env=settings.additional_env,
)

app.synth()
