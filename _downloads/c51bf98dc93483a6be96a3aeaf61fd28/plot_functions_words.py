"""
Words with Functions
====================

Scraping article text data and metadata, using a function oriented approach.
"""

###################################################################################################
#
# Function Approach: collect_words
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# MORE WORDS.
#

###################################################################################################

from lisc.collect import collect_words

###################################################################################################

terms = [['brain'], ['body']]

###################################################################################################

# Collect words data, setting the collection return data for at most 5 papers per term
dat, meta_data = collect_words(terms, retmax='5', usehistory=False,
                               save_and_clear=False, verbose=True)

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
