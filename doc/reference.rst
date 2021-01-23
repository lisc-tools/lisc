Reference and Reporting Information
===================================

This page describes how to reference and report on using this method for collecting and analyzing the scientific literature.

Table of Contents
-----------------
.. contents::
   :local:
   :backlinks: none

Reference
~~~~~~~~~

If you use this method please cite the following paper:

.. topic:: Reference

	Donoghue, T. (2018)  LISC: A Python Package for Scientific Literature Collection and Analysis.
	Journal of Open Source Software, 4(41), 1674. DOI: 10.21105/joss.01674

Direct link: https://doi.org/10.21105/joss.01674

Example Applications
~~~~~~~~~~~~~~~~~~~~

You can find a list of some exaple projects that LISC has been used for on the
`Projects <https://github.com/lisc-tools/Projects>`_ page.

You can also find a list of articles that cite the LISC paper at this
`Google scholar link <https://scholar.google.com/scholar?oi=bibs&hl=en&cites=17340181230798961012>`_.

Methods Reporting
~~~~~~~~~~~~~~~~~

If you use this module in your work, there is some information that should be included in the methods section.

Specifically, we recommend including the following information in the methods section:

- The version number of the module that was used (for example 0.1.1)
- Which databases were accessed, and what information was collected from them
- The date(s) that the data collection was performed
- Information about the state of the database at the time of collection
- The search terms used, including synonyms, inclusion, and exclusion words
- Any settings used in the API calls when collecting data, for example date ranges

This information can be kept track of by keeping a record of the code used to run the collection, and with the logging and meta data tracking available in the module.
