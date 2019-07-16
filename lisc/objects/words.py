"""Class for LISC word analysis: analyses of text data."""

from lisc.objects.base import Base
from lisc.scrape import scrape_words

###################################################################################################
###################################################################################################

class Words(Base):
    """Class for searching through words in the abstracts of specified papers.

    Attributes
    ----------
    results : list of Data() objects
        Results for each search term, stored in custom Words object.
    labels : list of str
        Labels for each result data attached to object.
    meta_data : MetaData() object
        Meta data information about the data scrape.
    """

    def __init__(self):
        """Initialize LISC Words() object."""

        Base.__init__(self)

        self.results = list()
        self.labels = list()
        self.meta_data = None


    def __getitem__(self, key):
        """Index into Words object with term result key.

        Parameters
        ----------
        key : str
            Term name to get from results data.

        Returns
        -------
        Data() object
            Data object for the requested result.
        """

        # Give up if object is empty
        if len(self.labels) == 0:
            raise IndexError('Object is empty - cannot index.')

        # Check if requested key is available
        try:
            ind = self.labels.index(key)
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

        self.results.append(new_result)
        self.labels.append(new_result.label)


    def run_scrape(self, db='pubmed', retmax=None, field='TIAB', api_key=None, use_hist=False,
                   save_n_clear=False, logging=None, folder=None, verbose=False):
        """Launch a scrape of words data.

        Parameters
        ----------
        db : str, optional, default: 'pubmed'
            Which pubmed database to use.
        retmax : int, optional
            Maximum number of records to return.
        field : str, optional, default: 'TIAB'
            Field to search for term within.
            Defaults to 'TIAB', which is Title/Abstract.
        api_key : str
            An API key for a NCBI account.
        use_hist : bool, optional, default: False
            Use e-utilities history: storing results on their server, as needed.
        save_n_clear : bool, optional, default: False
            Whether to save words data to disk per term as it goes, instead of holding in memory.
        logging : {None, 'print', 'store', 'file'}
            What kind of logging, if any, to do for requested URLs.
        folder : str or SCDB() object, optional
            Folder or database object specifying the save location.
        verbose : bool, optional, default: False
            Whether to print out updates.
        """

        self.results, self.meta_data = scrape_words(self.terms, self.exclusions,
                                                    db=db, retmax=retmax, field=field,
                                                    api_key=api_key, use_hist=use_hist,
                                                    save_n_clear=save_n_clear,
                                                    logging=logging, folder=folder,
                                                    verbose=verbose)
        self.labels = [dat.label for dat in self.results]