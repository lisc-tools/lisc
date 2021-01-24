=========================
LISC - Literature Scanner
=========================

|ProjectStatus|_ |Version|_ |BuildStatus|_ |Coverage|_ |License|_ |PythonVersions|_ |Publication|_

.. |ProjectStatus| image:: https://www.repostatus.org/badges/latest/active.svg
.. _ProjectStatus: https://www.repostatus.org/#active

.. |Version| image:: https://img.shields.io/pypi/v/lisc.svg
.. _Version: https://pypi.python.org/pypi/lisc/

.. |BuildStatus| image:: https://travis-ci.com/lisc-tools/lisc.svg
.. _BuildStatus: https://travis-ci.com/lisc-tools/lisc

.. |Coverage| image:: https://codecov.io/gh/lisc-tools/lisc/branch/master/graph/badge.svg
.. _Coverage: https://codecov.io/gh/lisc-tools/lisc

.. |License| image:: https://img.shields.io/pypi/l/lisc.svg
.. _License: https://opensource.org/licenses/Apache-2.0

.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/lisc.svg
.. _PythonVersions: https://pypi.python.org/pypi/lisc/

.. |Publication| image:: https://joss.theoj.org/papers/10.21105/joss.01674/status.svg
.. _Publication: https://doi.org/10.21105/joss.01674

LISC is a package for collecting and analyzing the scientific literature.

Overview
--------

LISC acts as a wrapper and connector between available APIs, allowing users to collect data from and
about scientific articles, and to do analyses on this data, such as performing automated meta-analyses.

A curated list of some projects enabled by LISC is available on the `projects <https://github.com/lisc-tools/Projects>`_ page.

Supported APIs
~~~~~~~~~~~~~~

Supported APIs through LISC includes:

- The NCBI `EUtils <https://www.ncbi.nlm.nih.gov/books/NBK25497/>`_ provides programmatic access to the National Center for Biotechnology Information (NCBI), including the Pubmed database.
- The `OpenCitations <https://opencitations.net>`_ API provides access to citation data.

Data Collection
~~~~~~~~~~~~~~~

The following types of literature data collection are currently supported:

- 'Counts': collects counts and co-occurrences of specified search terms in the literature.
- 'Words': collects text data and meta-data from articles identified by specified search terms.
- 'Citations': collect citation and reference data for articles, based on DOIs.

Analysis & Other Functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to connecting to external APIs, LISC also provides:

- Custom data objects for managing collected data
- A database structure, and save and load utilities for storing collected data
- Functions and utilities to analyze collected data
- Data visualization functions for plotting collected data and analysis outputs

Documentation
-------------

Documentation is available on the `documentation site <https://lisc-tools.github.io/lisc/>`_.

This documentation includes:

- `Tutorials <https://lisc-tools.github.io/lisc/auto_tutorials/index.html>`_:
  with a step-by-step guide through the module and how to use
- `Examples <https://lisc-tools.github.io/lisc/auto_examples/index.html>`_:
  demonstrating example analyses and use cases, and other functionality
- `API list <https://lisc-tools.github.io/lisc/api.html>`_:
  which lists and describes all the code and functionality available in the module
- `Reference <https://lisc-tools.github.io/lisc/reference.html>`_:
  with information for how to reference and report on using the module

For a curated list of projects that use LISC (or pre-cursors), check out the `projects <https://github.com/lisc-tools/Projects>`_ page.

Dependencies
------------

LISC is written in Python 3, and requires Python 3.5 or greater to run.

Requirements:

- `numpy <https://pypi.org/project/numpy/>`_
- `requests <https://pypi.org/project/requests/>`_
- `lxml <https://pypi.org/project/lxml/>`_
- `beautifulsoup4 <https://pypi.org/project/beautifulsoup4/>`_
- `nltk <https://pypi.org/project/nltk/>`_

Optional dependencies, used for plots, analyses & testing:

- `matplotlib <https://pypi.org/project/matplotlib/>`_
- `seaborn <https://pypi.org/project/seaborn/>`_
- `scipy <https://pypi.org/project/scipy/>`_
- `wordcloud <https://pypi.org/project/wordcloud/>`_
- `pytest <https://pypi.org/project/pytest/>`_

Install
-------

**Stable Release Version**

To install the latest stable release, you can install from pip:

.. code-block:: shell

    $ pip install lisc

LISC can also be installed with conda, from the conda-forge channel:

.. code-block:: shell

    $ conda install -c conda-forge lisc

**Development Version**

To get the development version (updates that are not yet published to pip), you can clone this repo.

.. code-block:: shell

    $ git clone https://github.com/lisc-tools/lisc

To install this cloned copy of LISC, move into the directory you just cloned, and run:

.. code-block:: shell

    $ pip install .

**Editable Version**

If you want to install an editable version, for making contributions, download the development
version as above, and run:

.. code-block:: shell

    $ pip install -e .

Reference
---------

If you use this code in your project, please cite
::
    Donoghue, T. (2018)  LISC: A Python Package for Scientific Literature Collection and Analysis.
    Journal of Open Source Software, 4(41), 1674. DOI: 10.21105/joss.01674

Direct Link: https://doi.org/10.21105/joss.01674

Contribute
----------

This project welcomes and encourages contributions from the community!

To file bug reports and/or ask questions about this project, please use the
`Github issue tracker <https://github.com/lisc-tools/lisc/issues>`_.

To see and get involved in discussions about the module, check out:

- the `issues board <https://github.com/lisc-tools/lisc/issues>`_ for topics relating to code updates, bugs, and fixes
- the `development page <https://github.com/lisc-tools/Development>`_ for discussion of potential major updates to the module

When interacting with this project, please use the
`contribution guidelines <https://github.com/lisc-tools/lisc/blob/master/CONTRIBUTING.md>`_
and follow the
`code of conduct <https://github.com/lisc-tools/lisc/blob/master/CODE_OF_CONDUCT.md>`_.
