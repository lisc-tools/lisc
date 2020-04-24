.. _api_documentation:

=================
API Documentation
=================

The following is a list of the publicly available objects and functions in LISC.

Many of the elements listed here are objects, as indicated by being in CamelCase.

If you click on the object names, it will take you to a new page describing their attributes and methods.

Table of Contents
=================
.. contents::
    :local:
    :depth: 2

.. currentmodule:: lisc

Collection Objects
------------------

Custom objects for collecting & analyzing literature data.

Counts Object
~~~~~~~~~~~~~

.. currentmodule:: lisc

.. autosummary::
    :toctree: generated/

    Counts

Words Object
~~~~~~~~~~~~
.. currentmodule:: lisc

.. autosummary::
    :toctree: generated/

    Words

Base Object
~~~~~~~~~~~

.. currentmodule:: lisc.objects.base

.. autosummary::
    :toctree: generated/

    Base

Data Objects
------------

Custom objects for storing extracted data.

Term Object
~~~~~~~~~~~

.. currentmodule:: lisc.data

.. autosummary::
    :toctree: generated/
    :template: data_object.rst

    Term

Articles Objects
~~~~~~~~~~~~~~~~

.. currentmodule:: lisc.data

.. autosummary::
    :toctree: generated/

    Articles
    ArticlesAll

Metadata Object
~~~~~~~~~~~~~~~

.. currentmodule:: lisc.data

.. autosummary::
    :toctree: generated/

    MetaData

Data Collection Functions
-------------------------

Functions for collecting data from supported APIs.

.. currentmodule:: lisc

.. autosummary::
    :toctree: generated/

    collect_info
    collect_counts
    collect_words
    collect_citations

URLs & Requests Objects
-----------------------

Object to manage URLs & requests.

URLs Objects
~~~~~~~~~~~~

URL management for supported APIs.

.. currentmodule:: lisc.urls

.. autosummary::
    :toctree: generated/

    URLs
    EUtils
    OpenCitations

Requester Object
~~~~~~~~~~~~~~~~

Request management for interacting with APIs.

.. currentmodule:: lisc.requester

.. autosummary::
    :toctree: generated/

    Requester

Analysis Functions
------------------

Functions to analyze collected data.

Normalization
~~~~~~~~~~~~~

.. currentmodule:: lisc.analysis.counts

.. autosummary::
    :toctree: generated/

    compute_normalization

Association
~~~~~~~~~~~

.. currentmodule:: lisc.analysis.counts

.. autosummary::
    :toctree: generated/

    compute_association_index

Plotting Functions
------------------

Plotting functions for collected data.

Counts
~~~~~~

.. currentmodule:: lisc.plts.counts

.. autosummary::
    :toctree: generated/

    plot_matrix
    plot_clustermap
    plot_dendrogram

Words
~~~~~

.. currentmodule:: lisc.plts.words

.. autosummary::
    :toctree: generated/

    plot_years
    plot_wordcloud

Utilities
---------

Utilities and file management.

File IO
~~~~~~~

.. currentmodule:: lisc.utils

.. autosummary::
    :toctree: generated/

    save_object
    load_object

Database Management
~~~~~~~~~~~~~~~~~~~

.. currentmodule:: lisc.utils

.. autosummary::
    :toctree: generated/

    SCDB
    create_file_structure
