# LISC - Literature Scanner

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Latest Version](https://img.shields.io/pypi/v/lisc.svg)](https://pypi.python.org/pypi/lisc/)
[![Build Status](https://travis-ci.org/lisc-tools/lisc.svg)](https://travis-ci.org/lisc-tools/lisc)
[![codecov](https://codecov.io/gh/lisc-tools/lisc/branch/master/graph/badge.svg)](https://codecov.io/gh/lisc-tools/lisc)
[![License](https://img.shields.io/pypi/l/lisc.svg)](https://opensource.org/licenses/Apache-2.0)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/lisc.svg)](https://pypi.python.org/pypi/lisc/)

LISC is a package for collecting and analyzing the scientific literature.

## Overview

LISC acts as a wrapper and connector between available APIs, allowing users to collect data from and about scientific articles, and to do analyses on this data, such as performing automated meta-analyses.

A curated list of some projects enabled by LISC is available on the [projects](https://github.com/lisc-tools/Projects) page.

#### Supported APIs

Supported APIs through LISC includes:
- the NCBI [EUtils](https://www.ncbi.nlm.nih.gov/books/NBK25497/). EUtils provides programmatic access to the National Center for Biotechnology Information (NCBI), including the Pubmed database.
- the [OpenCitations](https://opencitations.net) API. OpenCitations provides access to citation data.

#### Data Collection

For data collection, LISC currently offers support for the following 'types' of literature data collection:
- 'Counts': collects counts and co-occurrences of specified search terms in the literature.
- 'Words': collects text data and meta-data from articles identified by specified search terms.
- 'Citations': collect citation and reference data for articles, based on DOIs.

#### Analysis & Other Functionality

In addition to connecting to external APIs, LISC also provides:
- custom data objects for managing collected data
- a database structure, and save and load utilties for storing collected data
- functions and utilities to analyze collected data
- Data visualization functions for plotting collected data and analysis outputs

## Documentation

Documentation for LISC available [here](https://lisc-tools.github.io/lisc/).

The documentation also includes a set of [tutorials](https://lisc-tools.github.io/lisc/auto_tutorial/index.html).

For a curated list of projects that use LISC (or pre-cursors), check out the [projects](https://github.com/lisc-tools/Projects) page.

## Dependencies

LISC is written in Python 3, and requires Python 3.5 or greater to run.

Requirements:
- [numpy](https://pypi.org/project/numpy/)
- [requests](https://pypi.org/project/requests/)
- [lxml](https://pypi.org/project/lxml/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [nltk](https://pypi.org/project/nltk/)

Optional dependencies, used for plots, analyses & testing:
- [matplotlib](https://pypi.org/project/matplotlib/)
- [seaborn](https://pypi.org/project/seaborn/)
- [scipy](https://pypi.org/project/scipy/)
- [wordcloud](https://pypi.org/project/wordcloud/)
- [pytest](https://pypi.org/project/pytest/)

## Install

**Stable Release Version**

To install the latest stable release of lisc, you can install from pip:

`$ pip install lisc`

**Development Version**

To get the development version (updates that are not yet published to pip), you can clone this repo.

`$ git clone https://github.com/lisc-tools/lisc`

To install this cloned copy of LISC, move into the directory you just cloned, and run:

`$ pip install .`

**Editable Version**

If you want to install an editable version, for making contributions, download the development version as above, and run:

`$ pip install -e .`

## Bug Reports

Please use the [Github issue tracker](https://github.com/lisc-tools/lisc/issues) to file bug reports and/or ask questions about this project.

## Contribute

`LISC` welcomes and encourages contributions from the community!

If you have an idea of something to add to LISC, please start by opening an [issue](https://github.com/lisc-tools/lisc/issues).

When working on LISC, please follow the [Contribution Guidelines](https://github.com/lisc-tools/lisc/blob/master/CONTRIBUTING.md), and also make sure to follow our
[Code of Conduct](https://github.com/lisc-tools/lisc/blob/master/CODE_OF_CONDUCT.md).
