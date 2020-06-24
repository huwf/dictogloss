#! /usr/bin/env python3

import os
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Dictogloss",
    version="0.2.0",
    author="Huw Fryer",
    description="A tool for splitting media files to aid with language learning",
    url="https://github.com/huwf/dictogloss",
    long_description=long_description,
    packages=find_packages(),
    classifiers=[
        "Development status :: 3 - Alpha"
    ],
    entry_points={

    }
)





