"""
Tutorial 00: LISC Overview
==========================

An overview of the LISC code organization and approach.
"""

###################################################################################################
# LISC Overview
# -------------
#
# LISC, or 'Literature Scanner', is a module for collecting and analyzing scientific literature.
#
# LISC serves mainly as a wrapper around available application programmer interfaces (APIs)
# that provide access to databases of scientific literature and related data.
#
# In this overview, we will first introduce LISC, including the overall code structure,
# and how the module handles search terms, data, files, and requests.
#

###################################################################################################
# Available Analyses
# ~~~~~~~~~~~~~~~~~~
#
# The utility of LISC is based on the APIs that it accesses.
#
# Currently supported external APIs include:
#
# - the NCBI `EUtils <https://www.ncbi.nlm.nih.gov/books/NBK25500/>`_ API,
#   which provides access to the Pubmed database
# - the `OpenCitations <https://opencitations.net>`_ API,
#   which provides access to citation data
#
# There are different ways to interact with these APIs, which each provide different data.
#
# Data collection and analysis approaches available through LISC include:
#
# EUtils:
#   - counts: collect word co-occurrence data, counting how often terms occur together
#   - words: collect text data and meta-data from scientific articles
#
# OpenCitations:
#   - citations: collect citation data and counts of citations to and from articles
#

###################################################################################################
# LISC Objects
# ------------
#
# LISC is object oriented, meaning it uses objects to handle search terms and collect data.
#
# We will first explore the :class:`~.Base` object, which is the underlying object that is
# used for data collection and analyses with EUtils.
#
# Note that you will typically not use the :class:`~.Base` object directly,
# but it is the base object for the :class:`~.Counts` and :class:`~.Words` objects
# that we will use later.
#

###################################################################################################

# Import the Base object used in LISC
from lisc.objects.base import Base

###################################################################################################

# Initialize a base object
base = Base()

###################################################################################################
# Search Terms
# ------------
#
# To collect scientific articles and associated data, we first need to define search terms
# of interest to find relevant literature.
#
# Search terms in LISC are organized as lists of strings. Each new search terms should
# be it's own list.
#
# By default, search terms are exact term matches, meaning results need to contain exact
# matches to the given search terms.
#
# Terms can be added to the object with the :meth:`~.Base.add_terms` method.
#

###################################################################################################

# Set some search terms of interest
terms = [['chemistry'], ['biology']]

# Add terms to the object
base.add_terms(terms)

###################################################################################################

# Check the terms added to the base object
base.check_terms()

###################################################################################################
# Complex Search Terms
# --------------------
#
# So far, we have chosen some search terms, defined as single words, to use as queries,
# and added them to our object.
#
# Sometimes we might want more control than just using single words, in which case we might
# want to add synonyms and/or use include inclusions or exclusion words.
#
# Synonyms
# ~~~~~~~~
#
# To include synonyms, just add more entries to the input list of terms.
#
# Multiple strings within the same list are combined with the 'OR' operator. This means
# results will be returned if they include any of the given terms.
#
# For example, the set of search terms ['brain', 'cortex'] is interpreted as:
# '("brain"OR"cortex")'.
#
# Being able to include synonyms is the reason each term entry is itself a list.
#
# Inclusion & Exclusion Words
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Sometimes we might need to control the returned results, by specifically including
# or excluding certain topics or results. We can do so by adding 'inclusion' and/or
# 'exclusion' words.
#
# Inclusions words are words that must also appear for a result to be returned.
# Inclusions words are combined with the 'AND' operator, meaning entries
# will only be included if they also include these words.
#
# For example, the search terms ['brain', 'cortex'] with the inclusion word ['biology']
# is interpreted as '("brain"OR"cortex")AND("biology")'.
#
# Exclusions words are words that must not be included in a result for it to be returned.
# Exclusion words are combined with the 'NOT' operator, meaning entries
# will be excluded if they include these terms.
#
# For example, the search terms ['brain', 'cortex'] with the exclusion word ['body']
# is interpreted as '("brain"OR"cortex")NOT("body")'.
#
# Putting it all Together
# ~~~~~~~~~~~~~~~~~~~~~~~
#
# Synonyms, inclusion and exclusion words can all be used together.
# You can also specify synonyms for inclusion and exclusion words.
#
# For example, the following set of search term components:
#
# - search terms ['brain', 'cortex']
# - inclusion words ['biology', 'biochemistry']
# - exclusion words ['body', 'corporeal']
#
# All combine to give the search term of:
#
# - `'("brain"OR"cortex")AND("biology"OR"biochemistry")NOT("body"OR"corporeal")'`
#
# Inclusion and exclusion words should be lists of the same length as the number of
# search terms. Each inclusion and exclusion term is used for the corresponding search
# term, matched by index. An empty list is used to indicate that there are no inclusions
# or exclusions words for a given search term.
#
# Now let's update our set of terms, to include some synonyms, inclusions and exclusions.
#

###################################################################################################

# Set up a list of multiple terms, each with synonyms
terms = [['gene', 'genetic'], ['cortex', 'cortical']]

# Add the terms to our object
base.add_terms(terms)

###################################################################################################

# Set up inclusions and exclusions
#   Each is a list, that should be the same length as the number of terms
inclusions = [['brain'], ['body']]
exclusions = [['protein'], ['subcortical']]

# Add the inclusion and exclusions
base.add_terms(inclusions, 'inclusions')
base.add_terms(exclusions, 'exclusions')

###################################################################################################

# Check the loaded terms
base.check_terms()

###################################################################################################

# Check inclusion & exclusion words
base.check_terms('inclusions')
print('\n')
base.check_terms('exclusions')

###################################################################################################
# Labels
# ~~~~~~
#
# Since search terms can have multiple components, LISC also creates and uses 'labels'
# for each search term.
#
# By default, the label for each term is defined as the first word in the search term list.
# Custom labels can also be added to the object.
#

###################################################################################################

# Check the label for the current terms
base.labels

###################################################################################################
# Check Full Search Terms
# ~~~~~~~~~~~~~~~~~~~~~~~
#
# If you want to check what the full search term will be, the :meth:`~.Base.make_search_term`
# can be used to create the combined term.
#
# Note that terms can be accessed using either their index or their label.
#

###################################################################################################

# Print out the full search terms
print(base.make_search_term(0))
print(base.make_search_term('cortex'))

###################################################################################################
# LISC Objects
# ~~~~~~~~~~~~
#
# Though LISC offers an object-oriented approach, all the core procedures used for
# collecting and analyzing data are implemented and available as stand-alone functions.
#
# The objects serve primarily to help organize the data and support common analyses.
#
# If you prefer, you can use the functions directly, which may be useful for custom
# analyses. To see examples of using the function, see the Examples page.
#

###################################################################################################
# Database Management
# -------------------
#
# When collecting and analyzing the scientific literature, there can be a lot of data,
# and therefore a lot of files, to keep track of.
#
# To address this, LISC proposes a database structure for organizing collected data.
#
# Using this structure is not required to use LISC, but if you do use it, then LISC functions
# and objects can automatically load and save files to a known and organized output structure.
#
# In some of the example, you will see the :class:`~.SCDB` database object, which
# stores the organization for a LISC database.
#

###################################################################################################

# Import a helper function to create a LISC file structure
from lisc.io import create_file_structure

###################################################################################################
#
# We can use :func:`~.create_file_structure` to create a LISC file structure.
#
# When called without any inputs, a database structure is created in the current directory.
#

###################################################################################################

# Create a database file structure
db = create_file_structure()

###################################################################################################

# Check the file structure for the created database
db.check_file_structure()
