"""
Tutorial 05: Collecting Citation Data
=====================================

Collecting citation data from OpenCitations.
"""

###################################################################################################
# References & Citations
# ----------------------
#
# Citation data, such as the list of articles a paper cites, and how many citations it
# receives, can be another useful measure for investigating the scientific literature.
# Unfortunately, citation data has historically been hard to access and investigate, due to
# a lack of available databases and APIs that provide access to such information.
#
# OpenCitations Project
# ~~~~~~~~~~~~~~~~~~~~~
#
# Recently, citation data has become more available with the
# `OpenCitations <https://opencitations.net>`_ project, which
# is an initiative to support and provide open bibliographic and citation data.
#
# The OpenCitations project maintains a database of citation data, and provides an API.
# that can be accessed using LISC.
#
# The main function for accessing the OpenCitations API is :func:`~.collect_citations`.
#

###################################################################################################

# Import the function used to access the OpenCitations API
from lisc.collect import collect_citations

###################################################################################################
# OpenCitations API
# -----------------
#
# The OpenCitations `API <https://opencitations.net/index/coci/api/v1>`_ offers multiple
# utilities to collect citation and reference data.
#
# Articles of interest can be searched for in the OpenCitations database using their
# `DOIs <https://en.wikipedia.org/wiki/Digital_object_identifier>`_.
#
# LISC supports collecting the number of citations and references, as well as lists of DOIs
# that cite or are cited by requested articles.
#
# In the following example, we will specify some DOIs or articles of interest, and collect
# citation and reference information about them with OpenCitations.
#

###################################################################################################

# Set up a list of DOIs to collect data for
dois = ['10.1007/s00228-017-2226-2', '10.1186/1756-8722-6-59']

###################################################################################################
# Citation Data
# -------------
#
# Citations refers to articles that are cited by a specified article.
#
# To do so, we need to pass our list of DOIs to the :func:`~.collect_citations` function.
# To get citations for these DOIs, we will use the 'citations' operation, which we specify
# by setting the 'util' argument to 'citations'.
#

###################################################################################################

# Collect citation data from OpenCitations
n_citations, meta_data = collect_citations(dois, util='citations')

###################################################################################################
#
# By default, :func:`~.collect_citations` returns a dictionary which stores the number
# of citations per input DOI, as well as a :class:`~.MetaData` object describing the collection.
#

###################################################################################################

# Check out the number of citations per DOI
for doi, n_cite in n_citations.items():
    print('{:25s} \t : {}'.format(doi, n_cite))

###################################################################################################
#
# You can also specify to collect DOIs of the papers that cite papers of interest.
#
# To do so, set the `collect_dois` argument to True, in which case an additional dictionary
# storing the DOIs of the articles that cite the searched for article(s) will be returned.
#

###################################################################################################

# Collect citations, including the list of cited DOIs
n_cites, cite_dois, meta_data = collect_citations(dois, util='citations', collect_dois=True)

###################################################################################################

# Check the collected list of citing DOIs
cite_dois[dois[0]]

###################################################################################################
# Reference Data
# --------------
#
# Instead of searching for citations to specified articles, we can also search for
# references, which refers to articles that are cited by the specified article(s).
#
# To do so, set the `util` argument to use the 'references' operation.
#

###################################################################################################

# Collect reference data
n_references, ref_dois, meta_data = collect_citations(dois, util='references', collect_dois=True)

###################################################################################################

# Check out the number of references per DOI
for doi, n_refs in n_references.items():
    print('{:25s} \t : {}'.format(doi, n_refs))

###################################################################################################
# Additional Operations
# ---------------------
#
# There is additional information in the OpenCitations database, including meta-data- on
# individual articles that are cited and included in references.
#
# This information is not yet accessible through LISC. Contributions are always
# welcome to extend the functionality. If you might be interested, feel free to get in
# touch on `Github <https://github.com/lisc-tools/lisc>`_.
#
