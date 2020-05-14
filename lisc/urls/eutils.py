"""EUtils URLs for LISC.

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

Utilities
---------
EInfo : Returns a list of all databases, and some basic data about them.
    settings - db, retmode
EGQuery : Returns the number of records in all databases by a single query.
    settings - term
ESearch : Returns UIDs matching a text query, or posts to / gets from history server.
    settings - db, field, term
EFetch : Returns formatted data records for a list of UIDs.
    settings - db, id, rettype, retmode

Settings
--------
db : the target database.
    Most relevant database are: 'pubmed' & 'pmc'
        - pubmed: is a database of over 25 million references
        - pmc: an archive of freely available full text articles
    More info here: https://www.nlm.nih.gov/pubs/factsheets/dif_med_pub.html
    FAQ on PMC: https://www.ncbi.nlm.nih.gov/pmc/about/faq/#q1
id : list of UIDs (comma separated).
field : the search field to search within.
retmax : maximum number of records to return.
retmode : format to return.
usehistory : whether to store findings on remote server.
term : search terms to use.
"""

from lisc.urls.urls import URLs

###################################################################################################
###################################################################################################

def get_wait_time(authenticated):
    """Get the wait time based on whether EUtils API use is authenticated or not.

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
    More information on rate limits is available here: https://www.ncbi.nlm.nih.gov/books/NBK25497/
    """

    return 1/10 if authenticated else 1/3


class EUtils(URLs):
    """URLs for the NCBI EUtils API.

    Attributes
    ----------
    base : str
        Base URL for the EUtils API.
    utils : dict
        The EUtil utilities.
    urls : dict
        URLs for each EUtils utility.
    settings : dict
        Dictionary of all defined settings and their values.
    authenticated : bool
        Whether using an API key as an authenticated NCBI user.
    """

    def __init__(self, db=None, retmax=None, field=None, retmode=None,
                 usehistory='n', api_key=None):
        """Initialize the NCBI EUtils URLs, with provided settings.

        Parameters
        ----------
        db : str, optional
            Which database to access from EUtils.
        retmax : int, optional
            The maximum number of articles to return.
        field : str, optional
            The search field to search within.
        retmode : {'lxml', 'xml'}, optional
            The return format for the results.
        usehistory : {'n', 'y'}, optional
            Whether to use history caching on the EUtils server.
            'n' indicates 'no', do not use history. 'y' indicates 'yes', to use history.
        api_key : str, optional
            An API key for authenticated NCBI user account.

        Examples
        --------
        Initialize a ``EUtils`` URL object:

        >>> urls = EUtils(db='pubmed', retmax=5)
        """

        base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
        utils = {'info' : 'einfo.fcgi',
                 'query' : 'egquery.fcgi',
                 'search' : 'esearch.fcgi',
                 'fetch' : 'efetch.fcgi'}

        authenticated = bool(api_key)
        URLs.__init__(self, base, utils, authenticated=authenticated)

        # Collect settings, filling in with all defined settings / arguments
        self.fill_settings(db=db, usehistory=usehistory, retmax=str(retmax),
                           field=field, retmode=retmode, api_key=api_key)


    def authenticate(self, url):
        """Authenticate a URL for the EUtils API.

        Parameters
        ----------
        url : str
            URL to add authentication to.

        Returns
        -------
        str
            Authenticated URL.
        """

        return url + '&api_key=' + self.settings['api_key']
