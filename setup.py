"""Setup titiler."""

from setuptools import find_packages, setup

inst_reqs = [
    "aiocache[memcached]",
    "titiler==0.1.0a14",
    "mangum>=0.10.0",
    "rio-tiler-pds",
]

extra_reqs = {
    "deploy": [
        "aws-cdk.core==1.76.0",
        "aws-cdk.aws_lambda==1.76.0",
        "aws-cdk.aws_apigatewayv2==1.76.0",
        "aws-cdk.aws_apigatewayv2_integrations==1.76.0",
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
