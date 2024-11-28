"""Setup script for lisc."""

import os
from setuptools import setup, find_packages

# Get the current version number from inside the module
with open(os.path.join('lisc', 'version.py')) as version_file:
    exec(version_file.read())

# Load the long description from the README
with open('README.rst') as readme_file:
    long_description = readme_file.read()

# Load the required dependencies from the requirements file
with open("requirements.txt") as requirements_file:
    install_requires = requirements_file.read().splitlines()

setup(
    name = 'lisc',
    version = __version__,
    description = 'Literature Scanner',
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    python_requires = '>=3.7',
    author = 'Thomas Donoghue',
    author_email = 'tdonoghue.research@gmail.com',
    maintainer = 'Thomas Donoghue',
    maintainer_email = 'tdonoghue.research@gmail.com',
    url = 'https://github.com/lisc-tools/lisc',
    download_url = 'https://github.com/lisc-tools/lisc/releases',
    packages = find_packages(),
    license = 'Apache License, 2.0',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        ],
    platforms = 'any',
    keywords = ['web-scraping', 'meta-analysis', 'text-mining', 'scientific-publications',
                'literature-mining', 'literature-review'],
    install_requires = install_requires,
    tests_require = ['pytest'],
    extras_require = {
        'plot'     : ['matplotlib', 'seaborn', 'wordcloud'],
        'analysis' : ['scipy'],
        'all'      : ['matplotlib', 'seaborn', 'wordcloud', 'scipy'],
    },
    project_urls = {
        'Documentation' : 'https://lisc-tools.github.io/',
        'Bug Reports' : 'https://github.com/lisc-tools/lisc/issues',
        'Source' : 'https://github.com/lisc-tools/lisc',
    },
)
