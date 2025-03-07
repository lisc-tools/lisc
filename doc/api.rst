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
    Counts1D

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

Custom objects and related functions for storing and managing extracted data.

Term Object
~~~~~~~~~~~

.. currentmodule:: lisc.data

.. autosummary::
    :toctree: generated/
    :template: data_object.rst

    Term

Metadata Object
~~~~~~~~~~~~~~~

.. currentmodule:: lisc.data

.. autosummary::
    :toctree: generated/

    MetaData

Articles Objects
~~~~~~~~~~~~~~~~

.. currentmodule:: lisc.data

.. autosummary::
    :toctree: generated/

    Articles
    ArticlesAll

Articles Processing
~~~~~~~~~~~~~~~~~~~

.. currentmodule:: lisc.data.process

.. autosummary::
    :toctree: generated/

    process_articles

Data Collection Functions
-------------------------

Functions for collecting data from supported APIs.

EUtils
~~~~~~

.. currentmodule:: lisc

.. autosummary::
    :toctree: generated/

    collect_info
    collect_words
    collect_counts
    collect_across_time

OpenCitations
~~~~~~~~~~~~~

.. currentmodule:: lisc

.. autosummary::
    :toctree: generated/

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

Co-Occurrence Data
~~~~~~~~~~~~~~~~~~

.. currentmodule:: lisc.analysis.counts

.. autosummary::
    :toctree: generated/

    compute_normalization
    compute_association_index
    compute_similarity

Words Data
~~~~~~~~~~

.. currentmodule:: lisc.analysis.words

.. autosummary::
    :toctree: generated/

    get_all_values
    get_all_counts
    get_attribute_counts

Plotting Functions
------------------

Plotting functions for collected data.

Counts
~~~~~~

.. currentmodule:: lisc.plts.counts

.. autosummary::
    :toctree: generated/

    plot_matrix
    plot_vector
    plot_clustermap
    plot_dendrogram

Words
~~~~~

.. currentmodule:: lisc.plts.words

.. autosummary::
    :toctree: generated/

    plot_years
    plot_wordcloud

Time
~~~~

.. currentmodule:: lisc.plts.time

.. autosummary::
    :toctree: generated/

    plot_results_across_years

File Management
---------------

File management and input / output.

I/O
~~~

.. currentmodule:: lisc.io.io

.. autosummary::
    :toctree: generated/

    save_json
    load_json
    save_jsonlines
    parse_json_data
    load_txt_file
    load_api_key
    save_object
    load_object
    save_time_results
    load_time_results
    save_meta_data
    load_meta_data

Database Management
~~~~~~~~~~~~~~~~~~~

.. currentmodule:: lisc.io.db

.. autosummary::
    :toctree: generated/

    SCDB
    create_file_structure
    check_file_structure
    get_structure_info
    check_directory

File Utilities
~~~~~~~~~~~~~~

.. currentmodule:: lisc.io.utils

.. autosummary::
    :toctree: generated/

    check_ext
    get_files
