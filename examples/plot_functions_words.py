"""
Words with Functions
====================

Collect article text data and metadata, using a function oriented approach.
"""

###################################################################################################
#
# Function Approach: collect_words
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The core function for collecting words data is the `collect_words` function.
#
# Given a list of search terms, this function handles all the requests to collect the data.
#

###################################################################################################

# Import function to collect data
from lisc.collect import collect_words

###################################################################################################

# Set some terms to search for
terms = [['brain'], ['body']]

###################################################################################################

# Collect words data, setting the collection return data for at most 5 papers per term
dat, meta_data = collect_words(terms, retmax='5', usehistory=False,
                               save_and_clear=False, verbose=True)

###################################################################################################

# The meta data includes some information on the database from which data was collected
meta_data['db_info']

###################################################################################################

# The function returns a list of LISC Data objects
dat

###################################################################################################

# Each data object holds the data for the collected papers
d1 = dat[0]

###################################################################################################

# Print out some of the data
print(d1.n_articles, '\n')
print('\n'.join(d1.titles), '\n')
