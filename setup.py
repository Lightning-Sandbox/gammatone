# Copyright 2014 Jason Heeris, jason.heeris@gmail.com
#
# This file is part of the gammatone toolkit, and is licensed under the 3-clause
# BSD license: https://github.com/detly/gammatone/blob/master/COPYING
from setuptools import setup, find_packages

setup(
    name="Gammatone",
    version="1.0.1",
    author="Jason Heeris",
    packages=find_packages(exclude=["tests"]),
    install_requires=["numpy", "scipy", "matplotlib"],
    extras_require={"test": ["nose", "mock"]},
    entry_points={"console_scripts": ["gammatone = gammatone.plot:main"]},
)
