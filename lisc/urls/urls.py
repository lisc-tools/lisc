"""Base URL object for LISC.

Segments : section added to the URL, separated by '/'.
Settings : settings added to the URL, as key value pairs, following a '?' and added with '&'.
"""

from lisc.urls.utils import make_segments, make_settings

###################################################################################################
###################################################################################################

class URLs():
    """URLs for an API interface.

    Attributes
    ----------
    base : str
        Base URL for the API.
    utils : dict
        What utilities are available for the API.
    urls : dict
        The URLs for each utility.
    settings : dict
        The available settings for the API.
    authenticated : boolean
        Whether acting as an authenticated user for the API.
    """

    def __init__(self, base, utils={}, authenticated=None):
        """Initialize a URLs object.

        Parameters
        ----------
        base : str
            Base URL for the API.
        utils : dict
            Utilities for the utility, a dictionary with names and URL extensions.
        authenticated : bool
            Whether acting as an authenticated user for the API.
        """

        self.base = base
        utils['base'] = self.base
        self.utils = utils
        self.urls = {key : None for key in self.utils.keys()}
        self.settings = {}
        self.authenticated = authenticated


    def check_url(self, util):
        """Check the built URL for a specified utility.

        Parameters
        ----------
        util : str
            Which utility to check the URL for.
        """

        self._check_util(util)
        print(self.urls[util])


    def fill_settings(self, **kwargs):
        """Put all provided settings values into a dictionary object.

        Parameters
        ----------
        **kwargs
            Keyword arguments for all settings, with their values.

        Notes
        -----
        Potential parameters to this function include all the possible settings for the given API.

        Any possible setting that is provided a value as an input to this function is
        saved out to the dictionary of collected and available settings.
        """

        self.settings = {ke: va for ke, va in kwargs.items() if va is not None}


    def authenticate(self, url):
        """Method to authenticate a URL for a given API.

        Parameters
        ----------
        url : str
            URL to add authentification to.

        Returns
        -------
        str
            Authenticated URL.

        Notes
        -----
        This is a placeholder method, on the base URLs object, and should be
        overloaded by any API object that has authentification.

        When overloading this method, it should implement whatever is needed
        to authenticate a URL request for the specified API.
        """

        return url


    def build_url(self, util, segments=[], settings=[]):
        """Build the URL for a specified utility, with provided settings.

        Parameters
        ----------
        util : str
            Which utility to build the URL for.
        segments : list of str
            Segments to add to the URL.
        settings : dict or list of str
            Settings to use to build the URL.
            If list, the settings values are taken from the objects settings attribute.
        """

        self._check_util(util)

        if isinstance(settings, list):
            if not all(el in self.settings.keys() for el in settings):
                raise ValueError('Not all requested settings available - can not proceed.')
            settings = {ke : va for ke, va in self.settings.items() if ke in settings}

        url = self.base + make_segments([self.utils[util]] + segments) + make_settings(settings)

        if self.authenticated:
            url = self.authenticate(url)

        self.urls[util] = url


    def get_url(self, util, segments=[], settings={}):
        """Get a requested URL, with any additional segments or settings.

        Parameters
        ----------
        util : str
            Which utility to get the URL for.
        segments : list of str, optional
            Any additional segments to add to the URL.
        settings : dict, optional
            Any additional settings to add to the URL.

        Returns
        -------
        full_url : str
            The requested URL, with any extra segments and settings added.
        """

        if not util in self.utils.keys():
            self.build_url(util)

        url = self.urls[util]
        settings_join = '?' if not '?' in url else '&'

        full_url = url + make_segments(segments) + make_settings(settings, settings_join)

        return full_url


    def _check_util(self, util):
        """Check that a requested utility is valid.

        Parameters
        ----------
        util : str
            Name of the utility to check for.
        """

        if util not in self.utils.keys():
            raise ValueError('Specified utility not understood.')
