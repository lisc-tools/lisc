"""
Tutorial 05: Collecting Citation Data
=====================================

Collecting citation data from OpenCitations.
"""

###################################################################################################
#
# References & Citations
# ----------------------
#
# Other features of interest about scientific literature are references and citations.
#
# Which articles are cited by a particular article, and how many citations an article
# receives can be a useful measure to investigate the literature, and explore
# the propogation of ideas.
#
# Unfortunately, citation data has historically been hard to access and investigate, due to
# the lack of available databases and APIs that provide access to such information.
#
# OpenCitations Project
# ~~~~~~~~~~~~~~~~~~~~~
#
# Recently, citation data has become more available with the `OpenCitations <https://opencitations.net>`_
# project, which is an initiative to support and provide open bibliographic and citation data.
#
# The OpenCitations project maintains a database of citation data, and provides an API.
#

###################################################################################################

from lisc.collect import collect_citations

###################################################################################################
#
# OpenCitations API
# -----------------
#
# The OpenCitations `API <https://opencitations.net/index/coci/api/v1>`_ offers multiple
# utilities to collect citation and reference data.
#
# Articles of interest are specified to the OpenCitations API using
# `DOIs <https://en.wikipedia.org/wiki/Digital_object_identifier>`_.
#
# Currently, LISC supports collecting the number of citations and references
# for articles from OpenCitations, whereby articles are specified by their DOIs.
#

###################################################################################################

# Set up a list of DOIs to collect data for
dois = ['10.1007/s00228-017-2226-2', '10.1186/1756-8722-6-59']

###################################################################################################
#
# Citation Data
# -------------
#
# Citations refers to articles that are cited by a specified article.
#

###################################################################################################

# Collect citation data
citations, meta_data = collect_citations(dois, util='citations')

###################################################################################################

# Check out the number of citations per DOI
for doi, n_cites in citations.items():
    print('{:25s} \t : {}'.format(doi, n_cites))

###################################################################################################
#
# Reference Data
# --------------
#
# References refers to articles that are cited by a specified article.
#

###################################################################################################

# Collect reference data
references, meta_data = collect_citations(dois, util='references')

###################################################################################################

# Check out the number of references per DOI
for doi, n_refs in references.items():
    print('{:25s} \t : {}'.format(doi, n_refs))

###################################################################################################
#
# More Complex Data Collection
# ----------------------------
#
# Currently the 'collect' functions available in LISC support collecting counts of
# references and citations.
#
# The OpenCitations API tools do provide more information, including meta-data on individual
# articles that are cited and included in references.
#
# LISC is also very open to contributions. If you are interested in developing
# more LISC integration to help collect and analyze more citation related data,
# feel free to get involved with the project on `Github <https://github.com/lisc-tools/lisc>`_.
#
