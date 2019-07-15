"""
Tutorial 03 - Words Scraping
============================

Scraping literature data, collecting text and metadata for specified search terms.
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
from lisc import Words

###################################################################################################

# Set up some test data
#  Note that each entry should be a list
terms_a = [['brain'], ['cognition']]
terms_b = [['body'], ['biology'], ['disease']]

###################################################################################################
#
# Object Approach: Words
# ----------------------
#

###################################################################################################

# Initialize Words object and set the terms to search for
words = Words()
words.add_terms(terms_a)

###################################################################################################

# Run words scrape
words.run_scrape(retmax='5', save_n_clear=False)

###################################################################################################

# Words also saves the same list of Data objects
words.results

###################################################################################################
#
# The use of synonyms and exclusion words, demonstrated above for counts,
# applies in the same way to the scraping words.
#

###################################################################################################
#
# Metadata
# --------
#
# Regardless of what you are scraping, or how you run it through LISC,
# there is some meta-data saved.
#
# This data is collected in a dictionary, that is returned by the scrape
# functions (and saved to the objects, if applicable).

###################################################################################################

# This data is also saved to object
words.meta_data['db_info']

###################################################################################################
#
# It also includes the Requester object, which is used to launch URL requests
#
# This object also stores some details about the scrape
#
# It can be used, for example, to track how long scrapes take, and how many requests they include
#

###################################################################################################

print('Start time:    ', meta_data['req'].st_time)
print('End time:      ', meta_data['req'].en_time)
print('# of requests: ', meta_data['req'].n_requests)
