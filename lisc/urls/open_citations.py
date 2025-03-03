"""OpenCitations URLs for LISC.

External Documentation
----------------------
API Information:
    https://opencitations.net/index/coci/api/v1

Utilities
---------
references : Returns reference data for requested entries.
    settings - doi
citations : Returns citation data for requested entries.
    settings - doi
citation : Returns citation data for requested entries.
    settings - oci (Open Citation Identifier)
metadata : Returns metadata for
    settings - dois

Settings
--------
exclude : remove rows with empty values in the specified field name.
filter : a filtering operation to apply to returned data.
sort : a sort procedure to apply to returned data.
format : format to return data as, as either 'json' or 'csv'.
json : rules to transform returned json data.
"""

from lisc.urls.urls import URLs

###################################################################################################
###################################################################################################

class OpenCitations(URLs):
    """URLs for the OpenCitations API.

    Attributes
    ----------
    base : str
        Base URL for the OpenCitations API.
    utils : dict
        The OpenCitations utilities.
    urls : dict
        URLs for each OpenCitations utility.
    """

    def __init__(self):
        """Initialize the open citations urls object."""

        # Set up the base url & utils list for the open citations API
        base = 'https://w3id.org/oc/index/coci/api/v1'

        utils = {
            'references' : 'references',
            'citations' : 'citations',
            'metadata' : 'metadata',
        }

        URLs.__init__(self, base, utils)
