"""
Example - XXX
=============

XXXX.
"""

###################################################################################################
#
# Function Approach: scrape_words
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

###################################################################################################

from lisc.scrape import scrape_words

###################################################################################################

terms = ['brain', 'body']

###################################################################################################

# Scrape words data - set the scrape to return data for at most 5 papers per term
dat, meta_data = scrape_words(terms, retmax='5', use_hist=False, save_n_clear=False, verbose=True)

###################################################################################################

# The meta data includes some information on the database that was scraped
meta_data['db_info']

###################################################################################################

# The function returns a list of LISC Data objects
dat

###################################################################################################

# Each data object holds the data for the scraped papers
d1 = dat[0]

###################################################################################################

# Print out some of the data
print(d1.n_articles, '\n')
print('\n'.join(d1.titles), '\n')
