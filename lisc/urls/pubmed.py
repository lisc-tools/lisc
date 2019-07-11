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

from lisc.core.errors import InconsistentDataError

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


class URLS():
    """Class to hold URL information for SCANR project.

    Attributes
    ----------
    eutils : str
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
    args : dict()
        Dictionary of all arguments (settings & values) that can be used in e-utils URL.
    authenticated : boolean
        Whether using an API key as an authenticated NCBI user.
    api_key : str
        The API key, if operating as an authenticated user.
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
        retmax : str, optional
            The maximum number of papers to return.
        field : str, optional
            The search field to search within.
        retmode : {'lxml', 'xml'}, optional
            The return format for the results.
        api_key : str, optional
            An API key for authenticated NCBI user account.
        """

        # Set up the base url for NCBI E-Utils
        self.eutils = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

        # Initialize variables to store search and fetch URLs
        self.info = str()
        self.query = str()
        self.search = str()
        self.fetch = str()

        # Initialize dictionary to save settings, and add settings to it
        self.settings = dict()
        self.fill_settings(db=db, usehistory=usehistory, retmax=retmax,
                           field=field, retmode=retmode)

        # Initialize dictionary to save url arguments, and populate it from settings
        self.args = dict()
        self.fill_args()

        # Check for authentication (API key)
        if api_key:
            self.authenticated = True
            self.api_key = api_key
        else:
            self.authenticated = False
            self.api_key = None


    def auth_url(self, url):
        """Add api key to URL, if authenticated."""

        if self.authenticated:
            return url + '&api_key=' + self.api_key
        else:
            return url


    def check_args(self, args_to_use):
        """Checks whether the requested arguments are defined, so that they can be used.

        Parameters
        ----------
        args_to_use : list of str
            Requested arguments to check that they are defined.
        """

        # Check that all requested arguments are available. Catch and raise custom error if not.
        try:
            [self.args[arg] for arg in args_to_use]
        except KeyError:
            raise InconsistentDataError('Not all requested settings provided - can not proceed.')


    def build_url(self, util, args):
        """Build the URL for a specified e-utility, with provided arguments.

        Parameters
        ----------
        util : {'info', 'query', 'search', 'fetch'}
            Which e-utility to build the URL for.
        args : list of str
            Arguments to use to build the URL.
        """

        utils = {'info' : 'einfo.fcgi?',
                 'query' : 'egquery.fcgi?',
                 'search' : 'esearch.fcgi?',
                 'fetch' : 'efetch.fcgi?'}

        if util not in utils:
            raise ValueError('Specified e-utility not understood.')

        self.check_args(args)

        url = self.auth_url(self.eutils + utils[util])
        url = url + '&'.join([self.args[arg] for arg in args])

        if util in ['query', 'search']:
            url += '&term='

        setattr(self, util, url)


    def fill_settings(self, usehistory=None, db=None, retmax=None, field=None, retmode=None):
        """Put all provided settings values into a dictionary object.

        Parameters
        ----------
        db : str, optional
            Which database to use.
        retmax : str, optional
            Maximum number of items to return.
        field : str, optional
            The search field to search within.
        retmode :  {'lxml', 'xml'}, optional
            The return format for the results.

        Notes
        -----
        - All possible settings are set as possible arguments to this function.
            For each  possible settings, each that is given a value is saved out to the dictionary.
        - The 'locals()' function returns a dictionary of variables in scope (in this function).
        - Using 'locals()' saves separately defining a list of possible variables, that
            would need to be maintained to make sure it matched the method arguments.
        """

        # # Equivalent and more explicit to the dictionary comprehension below
        #
        # # Initialize list of possible settings, and remove the self argument
        # possible_settings = locals().keys()
        # possible_settings.remove('self')
        #
        # # Loop through all possible settings
        # for ps in possible_settings:
        #
        #     # If defined (not None) set the value of the setting
        #     #   into a dictionary, with key of the name of the setting
        #     if eval(ps):
        #         self.settings[ps] = eval(ps)

        self.settings = {ke: va for ke, va in locals().items() \
            if ke is not 'self' and va is not None}


    def fill_args(self):
        """Create the arguments that can be added to the e-utils urls."""

        # For each parameter in settings, create the url argument
        for param in self.settings.keys():
            self.args[param] = param + '=' + self.settings[param]
