"""LISC setup script."""

import os
from setuptools import setup, find_packages

# Get the current version number from inside the module
with open(os.path.join('lisc', 'version.py')) as vf:
    exec(vf.read())

long_description = \
"""
Literature Scanner.
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
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
    download_url = 'https://github.com/tomdonoghue/lisc/releases',
    keywords = ['web-scraping', 'meta-analysis', 'text-mining', 'scientific-publications', 'literature-mining', 'literature-review'],
    install_requires = ['numpy', 'nltk', 'beautifulsoup4', 'requests'],
    tests_require = ['pytest']
)