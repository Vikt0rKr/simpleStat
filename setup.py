# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="simpleStat",
    version="0.2.0",
    description="Parse Excel file to do math corellations.",
    license="MIT",
    author="Victor Krivonos",
    packages=find_packages(),
    install_requires=[
        'pandas>=0.24.2',
        'numpy>=1.16.2',
        'python-dateutil>=2.8.0',
        'pytz>=2018.9',
        'six>=1.12.0',
        'scipy>=1.2.1'
    ],
    entry_points={
        'console_scripts': ['start-app=src.__init__:start'],
    },
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ]
)
