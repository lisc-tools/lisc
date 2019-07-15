"""
Tutorial 01 - Counts Scraping
=============================

Scraping word co-occurence data from scientific literature.
"""

###################################################################################################
#
# Word Co-Occurence
# -----------------
#
# Specifically, it searches the literature, and checks how often terms of interest appear together.
#
#

###################################################################################################
#
# Counts
# ------
#
# 'Counts' scraping gets data about the co-occurence of terms of interest.
#

###################################################################################################

from lisc import Counts

from lisc.core.db import SCDB
from lisc.core.io import save_object

###################################################################################################

# Set up some test data
#  Note that each entry is itself a list
terms = [['brain'], ['cognition']]

###################################################################################################
#
# Count Object
# ------------
#
# There is also an OOP interface available in LISC,
# to organize the terms and data, and run scrapes.
#
# Note that the underlying code is the same - the count object ultimately calls
# the same scrape function as above.
#

###################################################################################################

# Initialize counts object & add the terms that we want to scrape
counts = Counts()
counts.add_terms(terms)

###################################################################################################

# Run scrape
counts.run_scrape(verbose=True)

###################################################################################################
#
# The Counts object also comes with some helper methods to check out the data.
#

###################################################################################################

# Check the highest associations for each term
counts.check_cooc()

###################################################################################################

# Check how many papers were found for each search term
counts.check_counts()

###################################################################################################

# Check the top term
counts.check_top()

###################################################################################################
#
# Co-occurence data - different word lists
#

###################################################################################################

terms = [['brain'], ['cognition']]
terms_b = [['body'], ['biology'], ['disease']]

###################################################################################################

# Initialize count object
counts = Counts()

###################################################################################################

# Set terms lists
#  Different terms lists are indexed by the 'A' and 'B' labels
counts.add_terms(terms_a, 'A')
counts.add_terms(terms_b, 'B')

###################################################################################################

# Scrape co-occurence data
counts.run_scrape()

###################################################################################################

# From there you can use all the same methods to explore the data
#  You can also specify which list to check
counts.check_cooc('A')
print('\n')
counts.check_cooc('B')

###################################################################################################

save_object(counts_two, 'tutorial_counts', SCDB('dat'))
