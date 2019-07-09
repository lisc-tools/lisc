"""Class for LISC word analysis: analyses of text data."""

from lisc.base import Base
from lisc.scrape import scrape_words

###################################################################################################
###################################################################################################

class Words(Base):
    """Class for searching through words in the abstracts of specified papers.

    Attributes
    ----------
    result_keys : list of str
        Keys for each result data attached to object.
    results : list of Data() objects
        Results for each search term, stored in custom Words object.
    """

    def __init__(self):
        """Initialize LISC Words() object."""

        # Inherit from Base Class
        Base.__init__(self)

        # Initialize a list to store results for all terms
        self.result_keys = list()
        self.results = list()

        # Initialize dictionary to store db info
        self.meta_data = dict()


    def __getitem__(self, key):
        """Index into Words object with term result key.

        Parameters
        ----------
        key : str
            Term name to get from results data.

        Returns
        -------
        Data
            Data object for the requested result.
        """

        # Give up if object is empty
        if len(self.result_keys) == 0:
            raise IndexError('Object is empty - cannot index.')

        # Check if requested key is available
        try:
            ind = self.result_keys.index(key)
        except ValueError:
            raise IndexError('Requested key not available in object.')

        return self.results[ind]


    def add_results(self, new_result):
        """Add a new Data results object.

        Parameters
        ----------
        new_result : Data() object
            Object with information about current term.
        """

        self.result_keys.append(new_result.label)
        self.results.append(new_result)


    def run_scrape(self, db='pubmed', retmax=None, field='TIAB', api_key=None,
                   use_hist=False, save_n_clear=False, verbose=False):
        """Launch a scrape of words data.

        Parameters
        ----------
        db : str, optional (default: 'pubmed')
            Which pubmed database to use.
        retmax : int, optional
            Maximum number of records to return.
        field : str, optional, default: 'TIAB'
            Field to search for term within.
            Defaults to 'TIAB', which is Title/Abstract.
        api_key : str
            An API key for a NCBI account.
        use_hist : bool, optional (default: False)
            Use e-utilities history: storing results on their server, as needed.
        save_n_clear : bool, optional (default: False)
            Whether to
        verbose : bool, optional (default: False)
            Whether to print out updates.
        """

        self.results, self.meta_data = scrape_words(self.terms, self.exclusions,
                                                   db=db, retmax=retmax, field=field,
                                                   api_key=api_key, use_hist=use_hist,
                                                   save_n_clear=save_n_clear, verbose=verbose)
        self.result_keys = [dat.label for dat in self.results]
