"""LISC setup script."""

import os
from setuptools import setup, find_packages

# Get the current version number from inside the module
with open(os.path.join('lisc', 'version.py')) as vf:
    exec(vf.read())

long_description = \
"""
TO DO.
"""

setup(
    name = 'lisc',
    version = __version__,
    description = 'Literature Scanner',
    long_description = long_description,
    author = 'Tom Donoghue',
    author_email = 'thomasdonoghue@hotmail.com',
    url = 'https://github.com/tomdonoghue/lisc',
    packages = find_packages(),
    license = 'TODO',
    classifiers = ['TODO'],
    download_url = 'https://github.com/tomdonoghue/lisc/releases',
    keywords = ['TODO'],
    install_requires = ['TODO'],
    tests_require = ['pytest'],
    #extras_require = TODO
)