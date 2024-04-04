=========================
LISC - Literature Scanner
=========================

|ProjectStatus| |Version| |BuildStatus| |Coverage| |License| |PythonVersions| |Publication|

.. |ProjectStatus| image:: https://www.repostatus.org/badges/latest/active.svg
   :target: https://www.repostatus.org/#active
   :alt: project status

.. |Version| image:: https://img.shields.io/pypi/v/lisc.svg
   :target: https://pypi.python.org/pypi/lisc/
   :alt: version

.. |BuildStatus| image:: https://github.com/lisc-tools/lisc/actions/workflows/build.yml/badge.svg
   :target: https://github.com/lisc-tools/lisc/actions/workflows/build.yml
   :alt: build status

.. |Coverage| image:: https://codecov.io/gh/lisc-tools/lisc/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/lisc-tools/lisc
   :alt: coverage

.. |License| image:: https://img.shields.io/pypi/l/lisc.svg
   :target: https://opensource.org/licenses/Apache-2.0
   :alt: license

.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/lisc.svg
   :target: https://pypi.python.org/pypi/lisc/
   :alt: python versions

.. |Publication| image:: https://joss.theoj.org/papers/10.21105/joss.01674/status.svg
   :target: https://doi.org/10.21105/joss.01674
   :alt: publication

LISC is a package for collecting and analyzing scientific literature.

Overview
--------

LISC wraps and combines existing APIs, allowing users to collect data from and about
scientific articles and perform analyses on this data, allowing for automated meta-analyses.

A curated list of some projects enabled by LISC is available on the
`projects <https://github.com/lisc-tools/Projects>`_ page.

Supported APIs & Collection Approaches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Supported APIs and data collection approaches include:

- The `EUtils <https://www.ncbi.nlm.nih.gov/books/NBK25497/>`_ API, which provides access to literature data,
  including the `Pubmed <https://pubmed.ncbi.nlm.nih.gov/about/>`_ database, from which counts, co-occurrences,
  text, and meta-data from scientific articles can be collected.
- The `OpenCitations <https://opencitations.net>`_ API, which provides access to citation data, from which
  citation and reference information can be collected.

Analysis & Other Functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to connecting to external APIs, LISC also provides:

- A database structure, and save and load utilities for storing collected data
- Custom data objects for managing and preprocessing collected data
- Functions and utilities to analyze collected data
- Data visualization functions for plotting collected data and analysis outputs

Documentation
-------------

Documentation is available on the
`documentation site <https://lisc-tools.github.io/lisc/>`_.

This documentation includes:

- `Tutorials <https://lisc-tools.github.io/lisc/auto_tutorials/index.html>`_:
  with a step-by-step guide through the module and how to use it
- `Examples <https://lisc-tools.github.io/lisc/auto_examples/index.html>`_:
  demonstrating example analyses and use cases, and other functionality
- `API list <https://lisc-tools.github.io/lisc/api.html>`_:
  which lists and describes all the code and functionality available in the module
- `Reference <https://lisc-tools.github.io/lisc/reference.html>`_:
  with information for how to reference and report on using the module

For a curated list of projects that use LISC, see the
`projects <https://github.com/lisc-tools/Projects>`_ page.

Dependencies
------------

LISC is written in Python 3, and requires Python >= 3.7 to run.

Requirements:

- `numpy <https://pypi.org/project/numpy/>`_
- `requests <https://pypi.org/project/requests/>`_
- `lxml <https://pypi.org/project/lxml/>`_
- `beautifulsoup4 <https://pypi.org/project/beautifulsoup4/>`_

Optional dependencies, used for plotting, analyses & testing:

- `matplotlib <https://pypi.org/project/matplotlib/>`_
- `seaborn <https://pypi.org/project/seaborn/>`_
- `scipy <https://pypi.org/project/scipy/>`_
- `wordcloud <https://pypi.org/project/wordcloud/>`_
- `pytest <https://pypi.org/project/pytest/>`_

Install
-------

Stable releases of LISC are released on the Github
`release page <https://github.com/lisc-tools/lisc/releases>`_, and on
`PYPI <https://pypi.org/project/lisc/>`_.

Descriptions of updates and changes across versions are available in the
`changelog <https://lisc-tools.github.io/lisc/changelog.html>`_.

**Stable Release Version**

To install the latest stable release, you can install from pip:

.. code-block:: shell

    $ pip install lisc

LISC can also be installed with conda, from the conda-forge channel:

.. code-block:: shell

    $ conda install -c conda-forge lisc

**Development Version**

To get the development version (updates that are not yet published to pip), you can clone this repository.

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

If you use this code in your project, please cite:

.. code-block:: text

    Donoghue, T. (2018)  LISC: A Python Package for Scientific Literature Collection and Analysis.
    Journal of Open Source Software, 4(41), 1674. DOI: 10.21105/joss.01674

Direct Link: https://doi.org/10.21105/joss.01674

More information for how to cite this method can be found on the
`reference page <https://lisc-tools.github.io/lisc/reference.html>`_.

Contribute
----------

This project welcomes and encourages contributions from the community!

To file bug reports and/or ask questions about this project, please use the
`Github issue tracker <https://github.com/lisc-tools/lisc/issues>`_.

To see and get involved in discussions about the module, check out:

- the `issues board <https://github.com/lisc-tools/lisc/issues>`_
  for topics relating to code updates, bugs, and fixes
- the `development page <https://github.com/lisc-tools/Development>`_
  for discussion of potential major updates to the module

When interacting with this project, please use the
`contribution guidelines <https://github.com/lisc-tools/lisc/blob/main/CONTRIBUTING.md>`_
and follow the
`code of conduct <https://github.com/lisc-tools/lisc/blob/main/CODE_OF_CONDUCT.md>`_.
