# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='amca',
    version='0.0.1',
    description='An RL-based Backgammon agent.',
    long_description=readme,
    author='Abdul Rahman Dabbour, Omid Khorsand Kazemy, Yusuf Izmirlioglu',
    author_email='dabbour@sabanciuniv.edu, omidk@sabanciuniv.edu, yizmirlioglu@sabanciuniv.edu',
    url='https://github.com/ardabbour/amca',
    license=license,
    install_requires=['numpy', 'gym', 'tensorflow'],
    packages=find_packages(exclude=('tests', 'docs'))
)