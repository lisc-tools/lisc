"""
Tutorial 01 - Counts Scraping
=============================

Scraping term co-occurence data from scientific literature.
"""

###################################################################################################
#
# Term Co-Occurence
# -----------------
#
# Term co-occurence searches the literature, and checks how often terms of interest appear together.
#
# This type of analysis can be used to infer associations and relationships between
# terms of interest.
#

###################################################################################################

from lisc import Counts

from lisc.core.db import SCDB
from lisc.core.io import save_object

###################################################################################################
#
# Counts Object
# -------------
#
# The 'Counts' object is used to handle term co-occurence analyses.
#

###################################################################################################
#
# Counts: single list
# -------------------
#
# For the first example of running a counts analysis, we will use a single list of terms.
#
# When a single list of terms is provided, the word co-occurence is collected as the
# co-occurence of each term with every other term in the list.
#
# Let's start with an example using different parts of the brain, and examine
# how often these brain regions are talked about together.
#

###################################################################################################

# Set up some test data
terms = [['frontal lobe'], ['temporal lobe'], ['parietal lobe'], ['occipital lobe']]

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

# Check how many papers were found for each search term
counts.check_counts()

###################################################################################################

# Check the top term
counts.check_top()

###################################################################################################
#
# Counts: two lists
# -----------------
#
# In the first example above, we provided a single list of terms.
#
# Now let's explore using two different sets of terms.
#
# In this example, we will keep our list of brain regions, and explore how they
# might be related to different sensory systems.
#

###################################################################################################

# Set some new terms
terms_a = [['frontal lobe'], ['temporal lobe'], ['parietal lobe'], ['occipital lobe']]
terms_b = [['vision'], ['audition', 'auditory'], ['somatosensory'], ['olfaction', 'smell'],
           ['gustation', 'taste'], ['proprioception'], ['nociception', 'pain']]

###################################################################################################

# Set terms lists
#  Different terms lists are indexed by the 'A' and 'B' labels
counts.add_terms(terms_a, dim='A')
counts.add_terms(terms_b, dim='B')

###################################################################################################

# Scrape co-occurence data
counts.run_scrape()

###################################################################################################
#
# From there you can use all the same methods to explore the data
#

###################################################################################################

# Save out our counts object
save_object(counts, 'tutorial_counts', folder=SCDB('lisc_db'))
