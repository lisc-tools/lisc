# LISC - Literature Scanner

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Build Status](https://travis-ci.org/lisc-tools/lisc.svg)](https://travis-ci.org/lisc-tools/lisc)
[![codecov](https://codecov.io/gh/lisc-tools/lisc/branch/master/graph/badge.svg)](https://codecov.io/gh/lisc-tools/lisc)
[![License](https://img.shields.io/pypi/l/fooof.svg)](https://opensource.org/licenses/Apache-2.0)


LISC is a package for performing automated meta-analyses of scientific papers, built on top of the Pubmed E-Utils API.

NOTE: the current version is still a development version (0.1.0-dev) and may not be totally stable.

## Overview

LISC is a python module for collecting and analzying scientific literature. 

#### Data Collection

For data collection, LISC currently offers support for using the Pubmed E-Utilities.

LISC provides for two different 'types' of literature data collection:
- 'Counts': popularity and co-occurence analysis of specified search terms.
- 'Words': collects text data and meta-data from papers identified by specified search terms.

#### Data Analysis

LISC provides support and utities for:
- Custom data objects for managing and operating on returned data.
- Save and load utilties for storing collected data.
- Support and tools for analyzing and plotting returned data.
- Data visualization utilities.

## Documentation

Documentation for LISC available [here](https://lisc-tools.github.io/lisc/).

The documentation also includes a set of [tutorials](https://lisc-tools.github.io/lisc/auto_tutorial/index.html).

For a curated list of projects that use LISC (or pre-cursors), check out the [projects](https://github.com/lisc-tools/Projects) page.

## Dependencies

LISC is written in Python 3, and requires Python 3.4 or greater to run.

Requirements:
- numpy
- requests
- lxml
- beautifulsoup4
- nltk

Optional dependencies, used for plots & analysis:
- matplotlib
- seaborn
- scipy
- wordcloud

## Install

**Stable Release Version**

PIP install coming soon!

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
