#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re
from pathlib import Path

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version from `__init__.py`.
    """
    version = Path(package, "__init__.py").read_text()
    return re.search("__version__ = ['']([^'']+)['']", version).group(1)


def get_long_description():
    """
    Return the README.
    """
    long_description = ""
    with open("README.md", encoding="utf8") as f:
        long_description += f.read()
    long_description += "\n\n"
    with open("CHANGELOG.md", encoding="utf8") as f:
        long_description += f.read()
    return long_description


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [str(path.parent) for path in Path(package).glob("**/__init__.py")]


def read_file(filename):
    with io.open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines() if not line.startswith("#")]


setup(
    name="fastspeed",
    python_requires=">=3.6",
    version=get_version("fastspeed"),
    url="https://github.com/StudyExchange/fastspeed.git",
    project_urls={
        "Changelog": "https://github.com/StudyExchange/fastspeed.git/blob/master/CHANGELOG.md",
        "Source": "https://github.com/StudyExchange/fastspeed.git",
    },
    license="MIT",
    description="Fastspeed is a toolkit for serving LLM.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="StudyExchange",
    author_email="StudyExchange@163.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "fastspeed=fastspeed.main:main",
        ],
    },
    setup_requires=read_requirements("requirements-setup.txt"),
    install_requires=read_requirements("requirements-install.txt"),
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
