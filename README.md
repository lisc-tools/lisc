# LISC - Literature Scanner

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Build Status](https://travis-ci.org/lisc-tools/lisc.svg)](https://travis-ci.org/lisc-tools/lisc)
[![codecov](https://codecov.io/gh/lisc-tools/lisc/branch/master/graph/badge.svg)](https://codecov.io/gh/lisc-tools/lisc)
[![License](https://img.shields.io/pypi/l/fooof.svg)](https://opensource.org/licenses/Apache-2.0)


LISC is a package for performing automated meta-analyses of scientific papers, built on top of the Pubmed E-Utils API.

NOTE: the current version is still a development version (0.1.0-dev) and may not be totally stable.

## Overview

LISC is a python module for scraping literature data. It currently supports and acts as a wrapper around the Pubmed E-Utilities.

LISC provides for two different 'types' of scraping, 'Counts', which can be used to count the popularity and co-occurence of specified search terms, and 'Words', which collects meta-data and text data for papers identified from a set of search terms.

As well as the functionality to collect such data, LISC includes support to analyzing and plotting returned data, as well as save and load utilties for storing the collected data.

By construction, LISC provides both an Object-Oriented approach for running literature scrapes, as well as the option to use functions (both of which call the same underlying code).

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

LISC will be posted to PYPI soon.

For now, you can use it by cloning from Github. In terminal, run:

`$ git clone https://github.com/lisc-tools/lisc`

Once you have done this, move into the directory you just cloned and run:

`$ pip install .`
