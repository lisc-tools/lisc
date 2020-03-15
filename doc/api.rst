.. _api_documentation:

=================
API Documentation
=================

The following is a list of the publicly available objects and functions in LISC.

Many of the elements listed here are objects, as indicated by being in CamelCase.

If you click on the object names, it will take you to a new page describing their attributes and methods.

.. currentmodule:: lisc

Objects
-------

Custom objects for collecting & analyzing literature data.

.. currentmodule:: lisc.objects

.. autosummary::
  :toctree: generated/

  Counts
  Words

.. currentmodule:: lisc.objects.base

.. autosummary::
  :toctree: generated/

  Base

Data
----

Custom objects for storing extracted data.

.. currentmodule:: lisc.data

.. autosummary::
  :toctree: generated/

  Term
  Articles
  ArticlesAll
  MetaData

Collect
-------

Functions for collecting data from supported APIs.

.. currentmodule:: lisc.collect

.. autosummary::
  :toctree: generated/

  collect_info
  collect_counts
  collect_words
  collect_citations

URLs & Requests
---------------

Object to manage URLs & requests.

URLs
~~~~

URL management for supported APIs.

.. currentmodule:: lisc.urls

.. autosummary::
  :toctree: generated/

  URLs
  EUtils
  OpenCitations

Requester
~~~~~~~~~

Request management for interacting with APIs.

.. currentmodule:: lisc.requester

.. autosummary::
  :toctree: generated/

  Requester

Analysis
--------

Functions to analyze collected data.

Counts
~~~~~~

.. currentmodule:: lisc.analysis.counts

.. autosummary::
  :toctree: generated/

  compute_normalization
  compute_association_index

Plotting
--------

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

.. currentmodule:: lisc.utils.io

.. autosummary::
  :toctree: generated/

  save_object
  load_object

Database Management
~~~~~~~~~~~~~~~~~~~

.. currentmodule:: lisc.utils.db

.. autosummary::
  :toctree: generated/

  SCDB
  create_file_structure
