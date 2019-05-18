"""URLs for the LISC.

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
    args - ?
ESearch : Returns UIDs matching a text query, or posts to / gets from history server.
    args - db, term, field
EFetch : Returns formatted data records for a list of UIDs.
    args - ?

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

AUTH = False

###################################################################################################
###################################################################################################

class URLS(object):
    """Class to hold URL information for ERP SCANR project.

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
    """

    def __init__(self, db=None, usehistory='n', retmax=None, field=None,
                 retmode=None, auto_gen=False):
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
        auto_gen : boolean, optional
            Whether to automatically generate URLs (without extra arguments).
        """

        # Set up the base url for ncbi e-utils
        self.eutils = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

        # Initialize variables to store search and fetch URLs
        self.info = str()
        self.query = str()
        self.search = str()
        self.fetch = str()

        # Initialize dictionary to save settings, and add settings to it
        self.settings = dict()
        self.save_settings(db=db, usehistory=usehistory, retmax=retmax,
                           field=field, retmode=retmode)

        # Initialize dictionary to save url arguments, and populate it from settings
        self.args = dict()
        self.save_args()

        if auto_gen:
            self.build_search([])
            self.build_fetch([])


    def save_settings(self, usehistory=None, db=None, retmax=None, field=None, retmode=None):
        """Save provided setting values into a dictionary object.

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

        Equivalent and more explicit:

        # Initialize list of possible settings, and remove the self argument
        possible_settings = locals().keys()
        possible_settings.remove('self')

        # Loop through all possible settings
        for ps in possible_settings:

            # If defined (not None) set the value of the setting
            #   into a dictionary, with key of the name of the setting
            if eval(ps):
                self.settings[ps] = eval(ps)
        """

        # Save all defined settings to a dictionary
        self.settings = {k: v for k, v in locals().items() if k is not 'self' and v is not None}


    def save_args(self):
        """Create the arguments that can be added to the e-utils urls."""

        # For each parameter in settings, create the url argument
        for param in self.settings.keys():
            self.args[param] = param + '=' + self.settings[param]


    def check_args(self, args_to_use):
        """Checks whether the requested arguments are defined, so that they can be used.

        Parameters
        ----------
        args_to_use : list of str
            Requested arguments to check that they are defined.
        """

        # Check that all requested arguments are available. Catch and raise custom error if not
        try:
            [self.args[arg] for arg in args_to_use]
        except KeyError:
            raise InconsistentDataError('Not all requested settings provided - can not proceed.')


    def build_info(self, args_to_use):
        """Create the e-utils info URL, with specified arguments.

        Parameters
        ----------
        args_to_use : list of str
            Arguments to use to build the info URL.
        """

        # Check requested args are defined in settings
        self.check_args(args_to_use)

        # Set the eg query search url
        info_base = _check_auth(self.eutils + 'einfo.fcgi?')
        self.info = info_base + '&'.join([self.args[arg] for arg in args_to_use])


    def build_query(self, args_to_use):
        """Create the e-utils EGQuery URL, with specified arguments.

        Parameters
        ----------
        args_to_use : list of str
            Arguments to use to build the query URL.
        """

        # Check requested args are defined in settings
        self.check_args(args_to_use)

        # Set the eg query search url
        query_base = _check_auth(self.eutils + 'egquery.fcgi?')
        self.query = query_base + '&'.join([self.args[arg] for arg in args_to_use]) + '&term='


    def build_search(self, args_to_use):
        """Create the e-utils search URL, with specified arguments.

        Parameters
        ----------
        args_to_use : list of str
            Arguments to use to build the search URL.
        """

        # Check requested args are defined in settings
        self.check_args(args_to_use)

        # Set the search url
        search_base = _check_auth(self.eutils + 'esearch.fcgi?')
        self.search = search_base + '&'.join([self.args[arg] for arg in args_to_use]) + '&term='


    def build_fetch(self, args_to_use):
        """Create the e-utils fetch URL, with specified arguments.

        Parameters
        ----------
        args_to_use : list of str
            Arguments to use to build the fetch URL.
        """

        # Check requested args are defined in settings
        self.check_args(args_to_use)

        # Set the fetch url
        fetch_base = _check_auth(self.eutils + 'efetch.fcgi?')
        self.fetch = fetch_base + '&'.join([self.args[arg] for arg in args_to_use])

###################################################################################################
###################################################################################################

def _check_auth(url):
    """Check for authorization, if so add registered details."""

    if AUTH and _authenticate:
        return url + 'email=tdonoghue@ucsd&tool=ERPscanr&'
    else:
        return url

def _authenticate():
    """Check that user has permission to run as registered E-Utils tool."""

    import hashlib

    try:
        with open('.auth', 'r') as f:
            pw = f.read()
            pw = pw.strip('\n')

        pwh = hashlib.sha224(pw.encode()).hexdigest()
        chh = 'a28ffb33c70f372d8974c12424f605518f025c08e94663e705304298'

        if  pwh == chh:
            print('Authentification passed.')
            return True
        else:
            print('Authentification failed.')
            return False

    except:
        print('Authentification failed.')
        return False
