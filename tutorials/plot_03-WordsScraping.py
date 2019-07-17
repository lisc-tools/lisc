"""
Tutorial 03 - Words Scraping
============================

Collecting literature data, extracting text and metadata for specified search terms.
"""

###################################################################################################
#
# Words
# -----
#
# Another way to scrape the literature is to collect text and meta-data from
# all papers found for a given set of terms.
#

###################################################################################################

# Import LISC - Words
from lisc import SCDB, save_object
from lisc import Words

###################################################################################################
#
# Words Object
# ------------
#
# The 'Words' object is used to handle word analyses.
#
# Note that the same principles of organizing search terms, including
# how to synonyms and exclusion words, are the same as for the introduced
# in the first tutorial.
#

###################################################################################################

# Set up some terms
terms = [['brain'], ['body']]

###################################################################################################

# Initialize Words object and set the terms to search for
words = Words()
words.add_terms(terms)

###################################################################################################

# Run words scrape
words.run_scrape(retmax='5', save_n_clear=False)

###################################################################################################

# Words also saves the same list of Data objects
words.results

###################################################################################################
#
# NEW EXAMPLE
# -----------
#


###################################################################################################

# Set up some terms
terms = [['frontal lobe'], ['temporal lobe'], ['parietal lobe'], ['occipital lobe']]
words.add_terms(terms)

###################################################################################################

db = SCDB('lisc_db')

# Run words scrape
words.run_scrape(retmax='10', save_n_clear=True, folder=db)


save_object(words, 'tutorial_words', folder=db)
