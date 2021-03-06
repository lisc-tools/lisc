"""Class for LISC word analysis: analyses of text data."""

from lisc.objects.base import Base
from lisc.collect import collect_words

###################################################################################################
###################################################################################################

class Words(Base):
    """A class for collecting and analyzing words data for specified terms list(s).

    Attributes
    ----------
    results : list of Articles
        Results of 'Words' data for each search term.
    labels : list of str
        Labels for each data object attached to the object.
    meta_data : MetaData
        Meta data information about the data collection.
    """

    def __init__(self):
        """Initialize LISC Words object."""

        Base.__init__(self)

        self.results = list()
        self.meta_data = None


    @property
    def labels(self):
        """The labels for each term."""

        return [result.label for result in self.results]


    def __getitem__(self, key):
        """Index into Words object with term result key.

        Parameters
        ----------
        key : str
            Term name to get from results data.

        Returns
        -------
        Articles
            Articles object for the requested result.
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
        """Add new results for a term to the current object.

        Parameters
        ----------
        new_result : Articles
            Object with collected data for a specified term.
        """

        self.results.append(new_result)


    def run_collection(self, db='pubmed', retmax=None, field='TIAB', usehistory=False,
                       api_key=None, save_and_clear=False, logging=None,
                       directory=None, verbose=False, **eutils_kwargs):
        """Collect words data.

        Parameters
        ----------
        db : str, optional, default: 'pubmed'
            Which database to access from EUtils.
        retmax : int, optional
            Maximum number of records to return.
        field : str, optional, default: 'TIAB'
            Field(s) to search for term.
            Defaults to 'TIAB', which is Title/Abstract.
        usehistory : bool, optional, default: False
            Whether to use EUtils history, storing results on the EUtils server.
        api_key : str, optional
            An API key for a NCBI account.
        save_and_clear : bool, optional, default: False
            Whether to save words data to disk per term, instead of holding in memory.
        logging : {None, 'print', 'store', 'file'}, optional
            What kind of logging, if any, to do for requested URLs.
        directory : str or SCDB, optional
            Folder or database object specifying the save location for any outputs.
        verbose : bool, optional, default: False
            Whether to print out updates.
        **eutils_kwargs
            Additional settings for the EUtils API.

        Examples
        --------
        Collect words data for a set of terms, set to collect up to five articles each:

        >>> words = Words()
        >>> words.add_terms([['brain'], ['body']])
        >>> words.run_collection(retmax='5') # doctest: +SKIP
        """

        self.results, self.meta_data = collect_words(self.terms, self.inclusions, self.exclusions,
                                                     db=db, retmax=retmax, field=field, usehistory=usehistory,
                                                     api_key=api_key, save_and_clear=save_and_clear, logging=logging,
                                                     directory=directory, verbose=verbose, **eutils_kwargs)
