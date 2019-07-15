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
    author = 'Thomas Donoghue',
    author_email = 'tdonoghue.research@gmail.com',
    url = 'https://github.com/lisc-tools/lisc',
    packages = find_packages(),
    license = 'Apache License, 2.0',
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        ],
    download_url = 'https://github.com/lisc-tools/lisc/releases',
    keywords = ['web-scraping', 'meta-analysis', 'text-mining', 'scientific-publications', 'literature-mining', 'literature-review'],
    install_requires = ['numpy', 'nltk', 'beautifulsoup4', 'requests', 'lxml'],
    tests_require = ['pytest'],
    extras_require = {
        'plot'    : ['matplotlib', 'seaborn', 'wordcloud'],
        'analysis'   : ['scipy'],
        'all'     : ['matplotlib', 'seaborn', 'wordcloud', 'scipy']
    }
)