"""
Tutorial 00 - LISC Overview
===========================

An overview of the LISC code organization and approach.
"""

###################################################################################################
#
# Overview
# -----------
#
# In this overview tutorial, we will first explore the main aspects of LISC, and
# how it handles terms, data, files and requests.
#
# LISC serves as a wrapper around available application programmer interfaces (APIs)
# for interacting with databases that store scientific literature and related data.
#
# In this first overview, we will explore how LISC's code structure.
#

###################################################################################################
#
# Available Analyses
# ~~~~~~~~~~~~~~~~~~
#
# The functionality of LISC is dependent on the APIs that are supported.
#
# Currently supported external APIs include the NCBI EUtils, offering access to the Pubmed
# database, and the OpenCitations API, offering access to citation data.
#
# EUtils:
#   - Counts: collecting word co-occurence data, counting how often terms occur together.
#   - Words: collecting text data and meta-data from papers.
#
# OpenCitations:
#   - Cites: collecting citation data, counting the number of citations papers have
#

###################################################################################################
#
# LISC Objects
# ------------
#
# LISC is object oriented, meaning it offers and uses objects in order to handle
# search terms, collected data, and API requests.
#
# Here we will first explore the `Base` object, the underlying
# object structure for any data collections using search terms.
#
# Note that you will not otherwise use the `Base` object directly, but that it is the
# underlying object for the `Counts` and `Words` objects.
#

###################################################################################################

# Import the Base object
from lisc.objects.base import Base

###################################################################################################

# Initialize a base object
base = Base()

###################################################################################################
#
# Search Terms
# ------------
#
# For collecting papers and literature data, one first has to select search terms to
# find the literature of interest.
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
#
# Synonyms & Exclusion Words
# --------------------------
#
# So far, we have chosen some search terms to use as queries, and added them to our object.
#
# However, we often need more than just single search terms - we might want to
# also be able to specify synonyms and exclusion words.
#
# Synonyms are combined with the 'OR' operator, meaning results will
# be returned if they include any of the given terms.
#
# Exclusion words are combined with the 'NOT' operator, meaning entries
# will be excluded if they include these terms.
#
# For example, using search terms ['gene', 'genetic'] with exclusion words ['protein']
# creates the full search term: `'("gene"OR"genetic"NOT"protein")'`
#
# So let's update our set of terms, to include some synonyms and exclusions.
#

###################################################################################################

# Set up terms with synonyms
#  Being able to include synonyms is the reason each term entry is itself a list
terms = [['gene', 'genetic'], ['cortex', 'cortical']]

# Add the terms
base.add_terms(terms)

###################################################################################################

# Set up exclusions
#  You can also include synonyms for exclusions - which is why each entry is also a list
exclusions = [['protein'], ['subcortical']]

# Add the exclusions
base.add_terms(exclusions, 'exclusions')

###################################################################################################

# Check the loaded terms
base.check_terms()

###################################################################################################

# Check exclusion words
base.check_terms('exclusions')

###################################################################################################
#
# Labels
# ~~~~~~
#
# Since search terms with synonyms and exclusions are complex (have multiple parts), LISC
# will also create 'labels' for each search term, where the label for each term is the
# first item in each term list.
#

###################################################################################################

# Check the label for the current terms
base.labels

###################################################################################################
#
# On Objects
# ~~~~~~~~~~
#
# Though LISC offers an object-oriented approach, note that the core procedures available
# for scraping and analyzing data are implemented as stand-alone functions.
#
# The objects serve primarily to help organize the data and support common analyses.
#
# If you prefer, you can use the functions directly, in particular, for more custom approaches.
#
# See the examples page for some examples of using LISC directly with functions.
#

###################################################################################################
#
# Database Management
# -------------------
#
# When collecting and analysing literature, there can be a lot of data, and therefore
# a lot of files, to keep track of.
#
# For that reason, LISC offers a database structure
#
# If you use this file structure, LISC functions can automatically load and save files in an
# way using this file structure.
#

###################################################################################################

from lisc.core.db import SCDB, create_file_structure

###################################################################################################

# Create a database file structure.
#   Note that when called without a path argument input,
#   the folder structure is made in the current directory.
db = create_file_structure()

###################################################################################################

# Check the file structure for the created database
db.check_file_structure()
