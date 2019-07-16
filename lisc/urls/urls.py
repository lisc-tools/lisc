"""Base URL object for LISC"""

###################################################################################################
###################################################################################################

class URLS():
    """Class to hold URL information for SCANR project.

    Attributes
    ----------
    base : str
        Base URL for the API.
    utils : dict
        xx
    urls : dict
        xx
    authenticated : boolean
        xx
    """

    def __init__(self, base, utils, authenticated=None):

        self.base = base
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
        - All possible settings are set as possible arguments to this function.
            For each  possible settings, each that is given a value is saved out to the dictionary.
        """

        self.settings = {ke: va for ke, va in kwargs.items() if va is not None}


    def _check_util(self, util):
        """Check that a requested utility is valid."""

        if util not in self.utils.keys():
            raise ValueError('Specified utility not understood.')
