#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

from setuptools import setup

# Package meta-data.
NAME = "get-unblock"
DESCRIPTION = "Simple solution to convert synchronous calls to asynchronous for use in asynchronous programming"
URL = "https://github.com/abranjith/unblock"
EMAIL = "abranjith@gmail.com"
AUTHOR = "ranjith"
VERSION = "0.0.1"
README_CONTENT_TYPE = "text/markdown"

# What packages are required for this module to be executed?
REQUIRED = []

# here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with open("README.md", "r") as fh:
    long_description = fh.read()

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type=README_CONTENT_TYPE,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    python_requires=">=3.7.0",
    # If your package is a single module, use this instead of 'packages':
    packages=["unblock"],
    install_requires=REQUIRED,
    include_package_data=True,
    license="Apache-2.0",
    classifiers=[
        "License :: OSI Approved :: Apache-2.0 License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
