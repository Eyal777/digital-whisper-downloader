#! /usr/bin/env python3

import os
import re
from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, *parts), "r") as f:
        data = f.read()
    return data


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

setup(
    name="digital-whisper-download",
    version=find_version("digital-whisper-download", "version.py"),
    packages=find_packages(),
    license="GPL 2.0",
    description="small utility to download Digital Whisper's issues",
    long_description=readme
)
