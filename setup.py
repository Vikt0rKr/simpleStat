# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="simpleStat",
    version="0.1.0",
    description="Parse Excel file to do math corellations.",
    license="MIT",
    author="Victor Krivonos",
    packages=find_packages(),
    install_requires=[
        'Pandas=0.24.2'
    ],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ]
)
