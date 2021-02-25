"""Class for LISC word analysis: analyses of text data."""

from lisc.collect import collect_words
from lisc.objects.base import Base
from lisc.objects.utils import get_max_length

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


    def __getitem__(self, label):
        """Index into Words object, accessing results.

        Parameters
        ----------
        label : str
            Label for the term to get from results data.

        Returns
        -------
        Articles
            Articles object for the requested result.
        """

        if not self.has_data:
            raise IndexError('No data is available - cannot proceed.')

        try:
            ind = self.labels.index(label)
        except ValueError:
            raise IndexError('Requested label not available.')

        return self.results[ind]


    @property
    def has_data(self):
        """Indicator for if the object has collected data."""

        return bool(self.results)


    def add_results(self, new_result):
        """Add new results for a term to the current object.

        Parameters
        ----------
        new_result : Articles
            Object with collected data for a specified term.
        """

        self.results.append(new_result)
        self._add_term(new_result.term)


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

        self.results, self.meta_data = collect_words(self.terms, self.inclusions,
                                                     self.exclusions, self.labels,
                                                     db=db, retmax=retmax, field=field,
                                                     usehistory=usehistory, api_key=api_key,
                                                     save_and_clear=save_and_clear,
                                                     logging=logging, directory=directory,
                                                     verbose=verbose, **eutils_kwargs)


    def check_data(self):
        """Prints out the number of articles collected for each term."""

        twd = get_max_length(self.labels)
        print("Number of collected articles per term:")
        for label, data in zip(self.labels, self.results):
            print("\t{:{twd}} \t\t  {}".format(label, data.n_articles, twd=twd))


    def drop_data(self, n_articles):
        """Drop terms based on number of article results.

        Parameters
        ----------
        n_articles : int
            Minimum number of articles required to keep each term.

        Examples
        --------
        Drop terms with less than or equal to 20 articles (assuming `words` already has data):

        >>> words.drop_data(20) # doctest: +SKIP
        """

        inds = [ind for ind, res in enumerate(self.results) if res.n_articles < n_articles]

        for ind in list(reversed(sorted(inds))):
            self.drop_term(ind)
            self.results.pop(ind)
