from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open(Path(__file__).parent / "dagster_graphql/version.py", encoding="utf8") as fp:
        exec(fp.read(), version)

    return version["__version__"]


ver = get_version()
# dont pin dev installs to avoid pip dep resolver issues
pin = "" if ver == "1!0+dev" else f"=={ver}"
setup(
    name="dagster-graphql",
    version=ver,
    author="Dagster Labs",
    author_email="hello@dagsterlabs.com",
    license="Apache-2.0",
    description="The GraphQL frontend to python dagster.",
    url="https://github.com/dagster-io/dagster/tree/master/python_modules/dagster-graphql",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["dagster_graphql_tests*"]),
    include_package_data=True,
    python_requires=">=3.8,<3.13",
    install_requires=[
        "dagster==1.8.7",
        "graphene>=3,<4",
        "gql[requests]>=3,<4",
        "requests",
        "starlette",  # used for run_in_threadpool utility fn
    ],
    entry_points={"console_scripts": ["dagster-graphql = dagster_graphql.cli:main"]},
)
