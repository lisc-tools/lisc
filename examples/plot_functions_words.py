"""
Words with Functions
====================

Collect article text data and metadata, using a function oriented approach.
"""

###################################################################################################
# Function Approach: collect_words
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The function for collecting words data is :func:`~.collect_words`.
#
# Given a list of search terms, this function handles all the requests to collect the data.
#
# The parameters for `collect_words` are the same as described in the Words tutorial.
#
# Here we will briefly explore collecting data directly using the function approach.
#

###################################################################################################

# Import the function to collect words data
from lisc.collect import collect_words

###################################################################################################

# Set some terms to search for
terms = [['brain'], ['body']]

###################################################################################################

# Collect words data, setting to collect data for at most 5 articles per term
results, meta_data = collect_words(terms, retmax='5', usehistory=False,
                                   save_and_clear=False, verbose=True)

###################################################################################################

# The meta data includes some information on the database from which data was collected
meta_data['db_info']

###################################################################################################

# The collected data is returned as a list of Articles objects
print(results)

###################################################################################################

# Each `Articles` object holds the data for the collected articles for a given term
res1 = results[0]

###################################################################################################

# Print out some of the data
print(res1.n_articles, '\n')
print('\n'.join(res1.titles), '\n')

###################################################################################################
#
# To further explore the collected data, check out the documentation for the
# :class:`~.Articles` object. To aggregate data across articles, check out the
# :class:`~.ArticlesAll` object.
#
