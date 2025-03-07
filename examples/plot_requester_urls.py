"""
URLs and Requests
=================

Explore LISC utilities for managing URLs and requests.
"""

###################################################################################################
# URLs & Requests
# ---------------
#
# LISC uses custom objects to manage URLs and launch requests. These can be used to
# define how to interact with APIs of interest.
#
# For the main LISC functionality, you don't have to deal with these objects directly.
# They are used 'under the hood' by LISC functions for collecting data and interacting with
# APIs without requiring direct user interaction.
#
# In this example, we will explore using these objects directly, which may be useful for
# creating custom data collections, and/or to connect LISC with other APIs.
#

###################################################################################################

# Import the requester object
from lisc.requester import Requester

###################################################################################################
# Requester Object
# ~~~~~~~~~~~~~~~~
#
# The :class:`~.Requester` object uses the
# `requests <https://requests.readthedocs.io/>`_
# module to launch URL requests. It also adds some functionality such as throttling, to
# ensure requests respect API limits, as well as metadata collection and URL logging.
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
# The :class:`~.URLs` object is used in LISC to store URLs used for interacting with APIs.
#
# It includes functionality for using different utilities available through an API,
# and for storing and using different settings that may be available.
#
# In this example, we will explore using the the URLs object to access the
# `duckduckgo <https://duckduckgo.com>`_ API.
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
# The :class:`~.URLs` object can be used to create objects that support external APIs.
#
# LISC currently supports APIs for
# `EUtils <https://www.ncbi.nlm.nih.gov/books/NBK25500/>`_ and
# `OpenCitations <https://opencitations.net>`_.
#
# These are implemented as custom objects which are built on top of the :class:`~.URLs` object.
#

###################################################################################################

# Import URL objects for supported APIs
from lisc.urls import EUtils, OpenCitations

###################################################################################################

# Initialize EUtils API object
eutils = EUtils()

# Check what utilities are supported for the EUtils API
print(eutils.utils)

###################################################################################################

# Initialize an OpenCitations API object
citations = OpenCitations()

# Check what utilities are supported for the OpenCitations API
print(citations.utils)

###################################################################################################
# Adding New APIs
# ~~~~~~~~~~~~~~~
#
# The `EUtils` and `OpenCitations` objects can be used as examples for potentially adding
# new APIs to LISC. New API objects can be created by inheriting from the `URLs` object,
# and added information on the utilities and settings available for that particular API.
#
