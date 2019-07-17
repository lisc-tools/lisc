"""Pubmed URLs for LISC.

External Documentation
----------------------
EUtils Quick Start:
    http://www.ncbi.nlm.nih.gov/books/NBK25500/
EUtils in Depth:
    https://www.ncbi.nlm.nih.gov/books/NBK25499/
Usage Policies and Disclaimers:
    https://www.ncbi.nlm.nih.gov/home/about/policies.shtml
A list of all the valid databases:
    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi

Tools
-----
EInfo : Provides a list of all databases, and some basic data about them.
    args - db, retmode
EGQuery : Provides the number of records in all databases by a single query.
    args - ToDo
ESearch : Returns UIDs matching a text query, or posts to / gets from history server.
    args - db, term, field
EFetch : Returns formatted data records for a list of UIDs.
    args - ToDo

Settings
--------
db : The target database.
    Most relevant database are: 'pubmed' & 'pmc'
        - pubmed: is a database of over 25 million references
        - pmc: an archive of freely available full text papers, of around 3 million papers
    More info here: https://www.nlm.nih.gov/pubs/factsheets/dif_med_pub.html
    FAQ on PMC: https://www.ncbi.nlm.nih.gov/pmc/about/faq/#q1
term : word(s) to search for.
id : list of UIDs (comma separated).
field : the search field to search within.
retmax : Maximum number of records to return.
retmode : Format to return.
usehistory : Whether to store findings on remote server.
"""

from lisc.urls.urls import URLS

###################################################################################################
###################################################################################################

def get_wait_time(authenticated):
    """Get the wait time based on whether EUtils API use is autheticated or not.

    Parameters
    ----------
    authenticated : bool
        Whether EUtils API use is authenticated.

    Returns
    -------
    float
        Wait time to use between API calls, in seconds.

    Notes
    -----
    The wait time for requesting is set for the E-Utils API, which allows for:
    - 10 requests/second for authenticated users (using an API key)
    - 3 requests/second otherwise
    ToDo: check these values.
    """

    return 1/10 if authenticated else 1/3


class EUtils(URLS):
    """Class to hold URLs for the NCBI EUtils API.

    Attributes
    ----------
    base : str
        Base URL for the e-utils tools.
    info  : str
        URL for getting database information from e-utils.
    query : str
        URL for querying with e-utils.
    search : str
        URL for searching with e-utils.
    fetch  : str
        URL for fetching with e-utils.
    settings : dict()
        Dictionary of all defined settings and their values.
    authenticated : boolean
        Whether using an API key as an authenticated NCBI user.
    """

    def __init__(self, db=None, usehistory='n', retmax=None,
                 field=None, retmode=None, api_key=None):
        """Initialize the ncbi e-utils urls.

        Parameters
        ----------
        db : {'pubmed', 'pmc'}, optional
            Which literature database to use.
        usehistory : {'n', 'y'}
            Whether to use history caching on pubmed server.
        retmax : int, optional
            The maximum number of papers to return.
        field : str, optional
            The search field to search within.
        retmode : {'lxml', 'xml'}, optional
            The return format for the results.
        api_key : str, optional
            An API key for authenticated NCBI user account.
        """

        # Set up the base url & utils list for the EUtils API
        base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        utils = {'info' : 'einfo.fcgi?',
                 'query' : 'egquery.fcgi?',
                 'search' : 'esearch.fcgi?',
                 'fetch' : 'efetch.fcgi?'}

        authenticated = bool(api_key)
        URLS.__init__(self, base, utils, authenticated=authenticated)

        # Collect settings, filling in with all defined settings / arguments
        self.fill_settings(db=db, usehistory=usehistory, retmax=str(retmax),
                           field=field, retmode=retmode, api_key=api_key)


    def build_url(self, util, args):
        """Build the URL for a specified utility, with provided arguments.

        Parameters
        ----------
        util : str
            Which utility to build the URL for.
        args : list of str
            Arguments to use to build the URL.
        """

        self._check_util(util)

        for arg in args:
            if arg not in self.settings:
                raise ValueError('Not all requested arguments available - can not proceed.')

        args = ['api_key'] + args if self.authenticated else args
        url = self.base + self.utils[util] + \
            '&'.join([arg + '=' + self.settings[arg] for arg in args])

        self.urls[util] = url


    def get_url(self, util, additions={}):
        """Get a requested URL, with any additional arguments.

        Parameters
        ----------
        util : str
            Which utility to get the URL for.
        additions : dict, optional
            Any additional arguments to add to the URL.

        Returns
        -------
        full_url : str
            The requested URL, with any extra arguments added.
        """

        self._check_util(util)

        extra_args = '&'.join([ke + '=' + va for ke, va in additions.items()])
        extra_args = '&' + extra_args if extra_args else ''

        full_url = self.urls[util] + extra_args

        return full_url
