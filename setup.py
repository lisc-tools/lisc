"""LISC setup script."""

import os
from setuptools import setup, find_packages

# Get the current version number from inside the module
with open(os.path.join('lisc', 'version.py')) as vf:
    exec(vf.read())

long_description = \
"""
LISC, or 'literature scanner' is a package for collecting and analyzing scientific literature.

LISC acts as a wrapper and connector between available APIs, allowing users to collect data from
and about scientific articles, and to do analyses on this data, such as performing automated meta-analyses.

Supported APIs available through LISC include the NCBI EUtils which provides programmatic access to the
National Center for Biotechnology Information (NCBI), including the Pubmed database, and the
OpenCitations API, which provides access to citation data.

For data collection, LISC currently offers support for the following 'types' of literature data collection:

- 'Counts': collects counts and co-occurrences of specified search terms in the literature.
- 'Words': collects text data and meta-data from articles identified by specified search terms.
- 'Citations': collect citation and reference data for articles, based on DOIs.

In addition to connecting to external APIs, LISC also provides:

- custom data objects for managing collected data
- a database structure, and save and load utilties for storing collected data
- functions and utilities to analyze collected data
- data visualization functions for plotting collected data and analysis outputs
"""

setup(
    name = 'lisc',
    version = __version__,
    description = 'Literature Scanner',
    long_description = long_description,
    author = 'Thomas Donoghue',
    author_email = 'tdonoghue.research@gmail.com',
    maintainer = 'Thomas Donoghue',
    maintainer_email = 'tdonoghue.research@gmail.com',
    url = 'https://github.com/lisc-tools/lisc',
    download_url = 'https://github.com/lisc-tools/lisc/releases',
    packages = find_packages(),
    license = 'Apache License, 2.0',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        ],

    keywords = ['web-scraping', 'meta-analysis', 'text-mining', 'scientific-publications',
                'literature-mining', 'literature-review'],
    install_requires = ['numpy', 'nltk', 'beautifulsoup4', 'requests', 'lxml'],
    tests_require = ['pytest'],
    extras_require = {
        'plot'     : ['matplotlib', 'seaborn', 'wordcloud'],
        'analysis' : ['scipy'],
        'all'      : ['matplotlib', 'seaborn', 'wordcloud', 'scipy']
    },
    project_urls = {
        'Documentation' : 'https://lisc-tools.github.io/',
        'Bug Reports' : 'https://github.com/lisc-tools/lisc/issues',
        'Source' : 'https://github.com/lisc-tools/lisc'
    },
)