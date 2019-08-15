"""Class for LISC word analysis: analyses of text data."""

from lisc.objects.base import Base
from lisc.collect import collect_words

###################################################################################################
###################################################################################################

class Words(Base):
    """A class for collecting and analyzing words data for specified terms list(s).

    Attributes
    ----------
    results : list of Data object
        Results for each search term, stored in custom Words object.
    labels : list of str
        Labels for each result data attached to object.
    meta_data : MetaData object
        Meta data information about the data collection.
    """

    def __init__(self):
        """Initialize LISC Words object."""

        Base.__init__(self)

        self.results = list()
        self.meta_data = None

    @property
    def labels(self):
        return [result.label for result in self.results]

    def __getitem__(self, key):
        """Index into Words object with term result key.

        Parameters
        ----------
        key : str
            Term name to get from results data.

        Returns
        -------
        Data object
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
        """Add a new results object.

        Parameters
        ----------
        new_result : Data object
            Object with information about current term.
        """

        self.results.append(new_result)


    def run_collection(self, db='pubmed', retmax=None, field='TIAB', usehistory=False,
                       api_key=None, save_and_clear=False, logging=None,
                       directory=None, verbose=False):
        """Collect words data.

        Parameters
        ----------
        db : str, optional, default: 'pubmed'
            Which database to access from EUtils.
        retmax : int, optional
            Maximum number of records to return.
        field : str, optional, default: 'TIAB'
            Field to search for term within.
            Defaults to 'TIAB', which is Title/Abstract.
        usehistory : bool, optional, default: False
            Whether to use EUtils history, storing results on their server.
        api_key : str
            An API key for a NCBI account.
        save_and_clear : bool, optional, default: False
            Whether to save words data to disk per term as it goes, instead of holding in memory.
        logging : {None, 'print', 'store', 'file'}
            What kind of logging, if any, to do for requested URLs.
        directory : str or SCDB object, optional
            Folder or database object specifying the save location.
        verbose : bool, optional, default: False
            Whether to print out updates.
        """

        self.results, self.meta_data = collect_words(self.terms, self.inclusions, self.exclusions,
                                                     db=db, retmax=retmax, field=field,
                                                     usehistory=usehistory, api_key=api_key,
                                                     save_and_clear=save_and_clear, logging=logging,
                                                     directory=directory, verbose=verbose)
