# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu',
    author_email='dabbour@sabanciuniv.edu, omidk@sabanciuniv.edu, yizmirlioglu@sabanciuniv.edu',
    url='https://github.com/ardabbour/amca',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

