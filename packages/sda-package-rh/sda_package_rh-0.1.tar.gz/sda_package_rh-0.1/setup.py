#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='sda_package_rh',
    version='0.1',
    author='Radek Hofírek',

    packages=find_packages(),
    license='LICENSE.txt',
    include_package_data=True,
    description='Package for SDA Python course',
)
