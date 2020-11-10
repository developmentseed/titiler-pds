"""Setup titiler."""

from setuptools import find_packages, setup

inst_reqs = [
    "aiocache[memcached]",
    "titiler==0.1.0a10",
    "mangum>=0.10.0",
    "rio-tiler~=2.0.0rc1",
    "rio-tiler-pds~=0.4.0",
    "cogeo-mosaic>=3.0.0a17",
]

extra_reqs = {
    "deploy": [
        "docker",
        "aws-cdk.core",
        "aws-cdk.aws_lambda",
        "aws-cdk.aws_apigatewayv2",
        "aws-cdk.aws_ecs",
        "aws-cdk.aws_ec2",
    ],
    "test": ["pytest", "pytest-cov", "pytest-asyncio", "requests"],
}


setup(
    name="app",
    version="0.0.1",
    description=u"TiTiler for AWS Public Dataset",
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)
