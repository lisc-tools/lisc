"""
Tutorial 00 - LISC Overview
===========================

Words, words, words.
"""

###################################################################################################
#
# Overview
# -----------
#
# In this overview tutorial, we will first explore the main aspects of LISC, and
# how it handles data, terms, database structure and requests.
#
#

###################################################################################################
#
# Overview
# -----------
#
# LISC is object oriented. First
#
#


###################################################################################################

from lisc.objects.base import Base

###################################################################################################

# Initialize a base object
base = Base()

###################################################################################################

# Set some terms
terms = [['chemistry'], ['biology']]

###################################################################################################

base.add_terms(terms)

###################################################################################################

base.check_terms()

###################################################################################################
#
# Synonyms & Exclusion Words
# --------------------------
#
# There is also support for adding synonyms and exclusion words.
#
# Synonyms are combined with the 'OR' operator, meaning results will
# be returned if they include any of the given terms.
#
# Exclusion words are combined with the 'NOT' operator, meaning entries
# will be excluded if they include these terms.
#
# For example, using search terms ['gene', 'genetic'] with exclusion words ['protein'] creates the search:
# - ("gene"OR"genetic"NOT"protein")
#

###################################################################################################
#
#
# Let's update our set of terms.
#
#
#

###################################################################################################

# Set up terms with synonyms
#  Being able to include synonyms is the reason each term entry is itself a list
terms = [['gene', 'genetic'], ['cortex', 'cortical']]

# Set up exclusions
#  You can also include synonyms for exclusions - which is why each entry is also a list
exclusions = [['protein'], ['subcortical']]

# Set the terms & exclusions
base.add_terms(terms_lst, 'A')
base.add_exclusions(excl_lst, 'A')

###################################################################################################

# You can check which terms are loaded
base.check_terms()

###################################################################################################

# Check exclusion words
base.check_exclusions()

###################################################################################################

# LISC objects will use the first item of each terms lists as a label for that term
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
# Words, words, words.

from lisc import SCDB

###################################################################################################
#
# URLs & Requests
# ---------------
#
# Words, words, words.
#

###################################################################################################

from lisc.urls.pubmed import Urls
from lisc.requester import Requester
