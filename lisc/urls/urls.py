"""Base URL object for LISC.

Segments : section added to the URL, separated by '/'.
Settings : settings added to the URL, as key value pairs, following a '?' and added with '&'.
"""

from lisc.urls.utils import check_none, check_settings, make_segments, make_settings

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
    authenticated : bool
        Whether acting as an authenticated user for the API.
    """

    def __init__(self, base, utils, authenticated=None):
        """Initialize a URLs object.

        Parameters
        ----------
        base : str
            Base URL for the API.
        utils : dict
            Utilities for the utility, a dictionary with names and URL extensions.
        authenticated : bool, optional
            Whether acting as an authenticated user for the API.

        Examples
        --------
        Initialize a ``URLs`` object for the Github API:

        >>> urls = URLs('https://api.github.com', {'search_repos': "search/repositories"})
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

        Examples
        --------
        Check the URL that gets built for a Github repository search:

        >>> urls = URLs('https://api.github.com', {'search_repos': "search/repositories"})
        >>> urls.fill_settings(q='lisc', sort='stars', order='desc')
        >>> urls.build_url('search_repos', settings=['q', 'sort', 'order'])
        >>> urls.check_url('search_repos')
        https://api.github.com/search/repositories?q=lisc&sort=stars&order=desc
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

        Examples
        --------
        Provide settings for the query, sort, and order of a Github search:

        >>> urls = URLs('https://api.github.com', {'search_repos': "search/repositories"})
        >>> urls.fill_settings(q='lisc', sort='stars', order='desc')
        """

        self.settings = check_settings({ke: va for ke, va in kwargs.items() if va is not None})


    def authenticate(self, url):
        """Method to authenticate a URL for a given API.

        Parameters
        ----------
        url : str
            URL to add authentication to.

        Returns
        -------
        str
            Authenticated URL.

        Notes
        -----
        This is a placeholder method, on the base URLs object, and should be
        overloaded by any API object that has authentication.

        When overloading this method, it should implement whatever is needed
        to authenticate a URL request for the specified API.
        """

        return url


    def build_url(self, util, segments=None, settings=None):
        """Build the URL for a specified utility, with provided settings.

        Parameters
        ----------
        util : str
            Which utility to build the URL for.
        segments : list of str, optional
            Segments to add to the URL.
        settings : dict or list of str, optional
            Settings to use to build the URL.
            If list, the settings values are taken from the objects settings attribute.

        Examples
        --------
        Build the url for the Github API to search for a repository search:

        >>> urls = URLs('https://api.github.com', {'search_repos': "search/repositories"})
        >>> urls.fill_settings(q='lisc', sort='stars', order='desc')
        >>> urls.build_url('search_repos', settings=['q', 'sort', 'order'])
        """

        self._check_util(util)

        if isinstance(settings, list):
            if not all(el in self.settings.keys() for el in settings):
                raise ValueError('Not all requested settings available - can not proceed.')
            settings = {ke : va for ke, va in self.settings.items() if ke in settings}

        url = self.base + make_segments([self.utils[util]] + check_none(segments, [])) + \
            make_settings(check_none(settings, {}))

        if self.authenticated:
            url = self.authenticate(url)

        self.urls[util] = url


    def get_url(self, util, segments=None, settings=None):
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

        Examples
        --------
        Get the url built for a Github repository search:

        >>> urls = URLs('https://api.github.com', {'search_repos': "search/repositories"})
        >>> urls.fill_settings(q='lisc', sort='stars', order='desc')
        >>> urls.build_url('search_repos', settings=['q', 'sort', 'order'])
        >>> urls.get_url('search_repos')
        'https://api.github.com/search/repositories?q=lisc&sort=stars&order=desc'
        """

        if not util in self.utils.keys():
            self.build_url(util)

        url = self.urls[util]
        settings_join = '?' if not '?' in url else '&'

        full_url = url + make_segments(check_none(segments, [])) + \
            make_settings(check_none(settings, {}), settings_join)

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
