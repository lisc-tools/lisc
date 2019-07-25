"""
URLs and Requests
=================

WORDS, WORDS, WORDS.
"""

###################################################################################################
#
# URLs & Requests
# ---------------
#
# MORE WORDS.
#
# Note that to use the main LISC functionality, you probably don't
# have to deal with these objects directly.
#
# This example is for if WORDS WORDS WORDS.
#

###################################################################################################

from lisc.requester import Requester

###################################################################################################
#
# Requester Object
# ~~~~~~~~~~~~~~~~
#
# MORE WORDS.
#

###################################################################################################

# Initialize a requester object
req = Requester()

###################################################################################################

# Set the minimum wait time between requests
req.set_wait_time(0.5)

###################################################################################################

for url in ['https://www.google.com', 'https://www.yahoo.com', 'https://duckduckgo.com']:
    page = req.request_url(url)
    print('Collecting web page \t {} \t got status code \t {}'.format(page.url, page.status_code))

###################################################################################################

# Check details of the requester object
req.check()

###################################################################################################

# Get information from the requester object as a dictionary
print(req.as_dict())

###################################################################################################
#
# URLs Object
# ~~~~~~~~~~~
#
# MORE WORDS.
#

###################################################################################################

from lisc.urls import URLs

###################################################################################################

base_path = 'https://api.duckduckgo.com/'
urls = URLs(base_path, {'search' : ''})

###################################################################################################

# Build and check the search URL
urls.build_url('search', settings={'format': 'json'})
urls.check_url('search')

###################################################################################################

# Get
api_url = urls.get_url('search', settings={'q' : 'brain'})
print(api_url)

###################################################################################################

api_page = req.request_url(api_url)

###################################################################################################
#
# WORDS HERE.
#

###################################################################################################

# Check the source of the first search result
api_page.json()['AbstractSource']
