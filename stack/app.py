"""Construct App."""

import os
from typing import Any, List, Optional

import docker
from aws_cdk import aws_apigatewayv2 as apigw
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda, core
from config import stack_config


DEFAULT_ENV = dict(
    CPL_TMPDIR="/tmp",
    GDAL_CACHEMAX="75%",
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
        concurrent: Optional[int] = None,
        permissions: Optional[List[iam.PolicyStatement]] = None,
        layer_arn: Optional[str] = None,
        env: dict = {},
        code_dir: str = "./",
        **kwargs: Any,
    ) -> None:
        """Define stack."""
        super().__init__(scope, id, *kwargs)

        permissions = permissions or []

        lambda_env = DEFAULT_ENV.copy()
        lambda_env.update(env)

        lambda_function = aws_lambda.Function(
            self,
            f"{id}-lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=self.create_package(code_dir),
            handler="app.main.handler",
            memory_size=memory,
            reserved_concurrent_executions=concurrent,
            timeout=core.Duration.seconds(timeout),
            environment=lambda_env,
        )

        for perm in permissions:
            lambda_function.add_to_role_policy(perm)

        if layer_arn:
            layer_arn = layer_arn.format(region=self.region)
            lambda_function.add_layers(
                aws_lambda.LayerVersion.from_layer_version_arn(
                    self, layer_arn.split(":")[-2], layer_arn
                )
            )

        # defines an API Gateway Http API resource backed by our "dynamoLambda" function.
        api = apigw.HttpApi(
            self,
            f"{id}-endpoint",
            default_integration=apigw.LambdaProxyIntegration(handler=lambda_function),
        )
        core.CfnOutput(self, "Endpoint", value=api.url)

    def create_package(self, code_dir: str) -> aws_lambda.Code:
        """Build docker image and create package."""
        print("Creating lambda package [running in Docker]...")
        client = docker.from_env()

        print("Building docker image...")
        client.images.build(
            path=code_dir, dockerfile="Dockerfile", tag="lambda:latest",
        )

        print("Copying package.zip ...")
        client.containers.run(
            image="lambda:latest",
            command="/bin/sh -c 'cp /tmp/package.zip /local/package.zip'",
            remove=True,
            volumes={os.path.abspath(code_dir): {"bind": "/local/", "mode": "rw"}},
            user=0,
        )

        return aws_lambda.Code.asset(os.path.join(code_dir, "package.zip"))


app = core.App()

perms = []
if stack_config.buckets:
    perms.append(
        iam.PolicyStatement(
            actions=["s3:GetObject", "s3:HeadObject"],
            resources=[f"arn:aws:s3:::{bucket}*" for bucket in stack_config.buckets],
        )
    )

# Tag infrastructure
for key, value in {
    "Project": stack_config.name,
    "Stack": stack_config.stage,
    "Owner": stack_config.owner,
    "Client": stack_config.client,
}.items():
    if value:
        core.Tag.add(app, key, value)


LambdaStack(
    app,
    f"{stack_config.name}-{stack_config.stage}",
    memory=stack_config.memory,
    timeout=stack_config.timeout,
    concurrent=stack_config.max_concurrent,
    permissions=perms,
    env=stack_config.additional_env,
)

app.synth()
