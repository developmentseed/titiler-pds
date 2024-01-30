"""Setup titiler."""

from setuptools import find_packages, setup

inst_reqs = [
    "brotli-asgi>=1.1.0",
    "titiler.core>=0.7.0",
    "titiler.mosaic>=0.7.0",
    "titiler.application>=0.7.0",
    "tilebench",
    "rio-tiler-pds>=0.7.0,<1.0",
    "mangum>=0.10",
]

extra_reqs = {
    "deploy": [
        "aws-cdk.core==1.160.0",
        "aws-cdk.aws_lambda==1.160.0",
        "aws-cdk.aws_apigatewayv2==1.160.0",
        "aws-cdk.aws_apigatewayv2_integrations==1.160.0",
    ],
    "test": ["pytest", "pytest-cov", "pytest-asyncio", "requests"],
}


setup(
    name="titiler_pds",
    version="0.1.0",
    description="TiTiler for AWS Public Dataset",
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["stack*", "tests*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)
