"""
Tutorial 00: LISC Overview
==========================

An overview of the LISC code organization and approach.
"""

###################################################################################################
# LISC Overview
# -------------
#
# LISC - or 'Literature Scanner' - is a module for collecting and analyzing scientific literature.
#
# LISC serves mainly as a wrapper around available application programmer interfaces (APIs)
# that provide access to databases of scientific literature and related data.
#
# In this overview tutorial, we will first explore the main aspects of LISC, such as
# how it handles terms, data, files and requests, and the overall code structure.
#

###################################################################################################
# Available Analyses
# ~~~~~~~~~~~~~~~~~~
#
# The functionality of LISC comes from on the APIs that are supported.
#
# Currently supported external APIs include the NCBI EUtils, offering access to the Pubmed
# database, and the OpenCitations API, offering access to citation data.
#
# The data collection and analysis approaches available through LISC include:
#
# EUtils:
#   - Counts: collecting word co-occurrence data, counting how often terms occur together.
#   - Words: collecting text data and meta-data from scientific articles.
#
# OpenCitations:
#   - Citations: collecting citation data, counting the number of citations to and from articles.
#

###################################################################################################
# LISC Objects
# ------------
#
# LISC is object oriented, meaning it uses objects to handle search terms and collect data.
#
# Here we will first explore the :class:`~.Base` object, the underlying object
# used for data collections and analysis with EUtils.
#
# Note that you will not otherwise use the :class:`~.Base` object directly,
# but that it is the underlying object for the :class:`~.Counts` and
# :class:`~.Words` objects that we will use later.
#

###################################################################################################

from lisc.objects.base import Base

###################################################################################################

# Initialize a base object
base = Base()

###################################################################################################
#
# Search Terms
# ------------
#
# To collect scientific articles and associated data, we first need to use search
# terms to find the literature of interest.
#
# By default, LISC uses all search terms as used as exact term matches, which is
# indicated using double quotes, as "search term".
#

###################################################################################################

# Set some terms
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
# So far, we have chosen some search terms, as single terms, to use as queries,
# and added them to our object.
#
# Sometimes we might want more than just particular search words. We might want to
# specify synonyms and/or use include inclusions or exclusion words.
#
# Synonyms
# ~~~~~~~~
#
# To include synonyms, just add more entries to the input list of terms.
#
# Synonyms are combined with the 'OR' operator, meaning results will
# be returned if they include any of the given terms.
#
# For example, the set of search terms ['brain', 'cortex'] is interpreted as:
# '("brain"OR"cortex")'.
#
# Being able to include synonyms is the reason each term entry is itself a list.
#
# Inclusion & Exclusion Words
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Sometimes we might need to control the results that we get, by including inclusion
# and exclusion words.
#
# Inclusions words are words that must also appear in the document for a result
# to be returned. Inclusions words are combined with the 'AND' operator, meaning entries
# will only be included if they also include these words.
#
# For example, the search terms ['brain', 'cortex'] with the inclusion word ['biology']
# is interpreted as '("brain"OR"cortex")AND("biology")'.
#
# Exclusions words are words that must not be included in a result in order for it
# to be returned. Exclusion words are combined with the 'NOT' operator, meaning entries
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
# - `'("gene"OR"genetic)AND("biology"OR"biochemistry")NOT("body"OR"corporeal)'`
#
# Inclusion and exclusion words should be lists of the same length as the
# number of search terms. Each inclusion and exclusion term is used for the
# corresponding search term, matched by index. If there are no inclusions / exclusions
# for a given search term, leave it empty with an empty list.
#
# Now let's update our set of terms, to include some synonyms, inclusions and exclusions.
#

###################################################################################################

# Set up a list of multiple terms, each with synonyms
terms = [['gene', 'genetic'], ['cortex', 'cortical']]

# Add the terms
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
# Since search terms with synonyms and exclusions are complex, in that they have multiple parts,
# LISC also creates and uses 'labels' for each search term. The label for each term is the
# first word from the search term list.
#

###################################################################################################

# Check the label for the current terms
base.labels

###################################################################################################
# LISC Objects
# ~~~~~~~~~~~~
#
# Though LISC offers an object-oriented approach, all the core procedures used for
# collecting and analyzing data are implemented and available as stand-alone functions.
#
# The objects serve primarily to help organize the data and support common analyses.
#
# If you prefer, you can use the functions directly, in particular, for more custom approaches.
#
# See the examples page for some examples of using LISC directly with functions.
#

###################################################################################################
# Database Management
# -------------------
#
# When collecting and analyzing literature, there can be a lot of data, and therefore
# a lot of files, to keep track of.
#
# LISC offers a database structure. If you use this file structure, LISC functions
# can automatically load and save files to an organized output structure.
#

###################################################################################################

from lisc.utils.db import create_file_structure

###################################################################################################

# Create a database file structure.
#   When called without a path input, the folder structure is made in the current directory.
db = create_file_structure()

###################################################################################################

# Check the file structure for the created database
db.check_file_structure()
