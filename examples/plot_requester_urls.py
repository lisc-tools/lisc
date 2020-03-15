"""
URLs and Requests
=================

Exploring LISC utilities for managing URLs and requests.
"""

###################################################################################################
# URLs & Requests
# ---------------
#
# LISC uses custom objects to manage URLs, that can store how to interact with
# APIs, as well as a custom object to manage requests.
#
# Note that to use the main LISC functionality, you don't have to deal with these
# objects directly, as they are used 'under the hood' by LISC functions for collecting
# data and interacting APIs without requiring user interaction.
#
# This example can be used if you want to explore custom data collections, and/or to
# use LISC for other APIs.
#

###################################################################################################

# Import the requester object
from lisc.requester import Requester

###################################################################################################
# Requester Object
# ~~~~~~~~~~~~~~~~
#
# The :class:`~lisc.requester.Requester` object uses the
# `requests <https://2.python-requests.org/en/master/>`_
# module to launch URL requests, and adds some functionality such as throttling, to
# ensure requests respect API limits, as well as metadata collection, and URL logging.
#

###################################################################################################

# Initialize a requester object
req = Requester()

###################################################################################################

# Set the minimum wait time between requests
req.set_wait_time(0.5)

###################################################################################################

# Use the Requester object to request some web pages
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
# URLs Object
# ~~~~~~~~~~~
#
# The :class:`~lisc.urls.URLs` object is the base object used in LISC to store
# URLs to interact with APIs.
#
# It includes functionality to store and use different utilities available through
# an API, and store and use different settings.
#
# In the example, we can explore using the the URLs object for a new API, in this case
# the `duckduckgo <https://duckduckgo.com>`_ API.
#

###################################################################################################

# Import the URLs object
from lisc.urls import URLs

###################################################################################################

# Set the base path for an API to use
base_path = 'https://api.duckduckgo.com/'

# Create the URLs object for the API, specifying it has a search utility
urls = URLs(base_path, {'search' : ''})

###################################################################################################

# Build and check the search URL
urls.build_url('search', settings={'format': 'json'})
urls.check_url('search')

###################################################################################################

# Get the URL to launch a search request with a specified search term
api_url = urls.get_url('search', settings={'q' : 'brain'})
print(api_url)

###################################################################################################

# Request the URL with the requester object from before
api_page = req.request_url(api_url)

###################################################################################################

# Check the source of the first search result
api_page.json()['AbstractSource']

###################################################################################################
# Supported APIs
# ~~~~~~~~~~~~~~
#
# The :class:`~lisc.urls.URLs` object can be used to create objects that support external APIs.
#
# LISC currently supports APIs for
# `EUtils <https://www.ncbi.nlm.nih.gov/books/NBK25500/>`_ and
# `OpenCitations <https://opencitations.net>`_.
#
# These are implemented as custom objects built on top of the URLs object.
#

###################################################################################################

# Import URL objects for supported APIs
from lisc.urls import EUtils, OpenCitations

###################################################################################################

# Initialize an object for the EUtils API
eutils = EUtils()

# Check what utilities are supported for the EUtils API
print(eutils.utils)

###################################################################################################

# Initialize an object for the OpenCitations API
citations = OpenCitations()

# Check what utilities are supported for the OpenCitations API
print(citations.utils)

###################################################################################################
# Adding New APIs
# ~~~~~~~~~~~~~~~
#
# If you are interested in extending LISC to interact with additional APIs, then
# you can use the `EUtils` and `OpenCitations` objects as examples, and build a
# new API object by inheriting from and using the `URLs` object.
#
