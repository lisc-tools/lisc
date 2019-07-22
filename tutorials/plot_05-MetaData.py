"""
Tutorial 05 - MetaData
======================

Scraping citation data from OpenCitations.
"""

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
#

###################################################################################################

# This data is also saved to object
#words.meta_data['db_info']

###################################################################################################
#
# It also includes the Requester object, which is used to launch URL requests
#
# This object also stores some details about the scrape
#
# It can be used, for example, to track how long scrapes take, and how many requests they include
#

###################################################################################################

# print('Start time:    ', words.meta_data.requester['st_time'])
# print('End time:      ', words.meta_data.requester['en_time'])
# print('# of requests: ', words.meta_data.requester['n_requests'])
