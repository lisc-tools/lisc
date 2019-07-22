"""OpenCitations URLs for LISC.

API Information:
https://opencitations.net/index/coci/api/v1

Operations
- references
- citations
- citation
- metadata

Parameters
- exclude
- filter
- sort
- format
- json
"""

from lisc.urls.urls import URLs

###################################################################################################
###################################################################################################

class OpenCitations(URLs):
    """Class to hold URLs for the OpenCitations API.

    Attributes
    ----------
    base : str
        Base URL for the OpenCitations API.
    utils : dict
        Collection of OpenCitations utilities.
    urls : dict
        URLs for each OpenCitations utility.
    """

    def __init__(self):
        """Initialize the open citations urls object."""

        # Set up the base url & utils list for the open citations API
        base = 'https://w3id.org/oc/index/coci/api/v1'

        utils = {'references' : 'references',
                 'citations' : 'citations',
                 'metadata' : 'metadata'}

        URLs.__init__(self, base, utils)
