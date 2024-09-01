"""Class for LISC word analysis: analyses of text data."""

from lisc.collect import collect_words
from lisc.objects.base import Base
from lisc.utils.base import get_max_length
from lisc.data.articles_all import ArticlesAll

###################################################################################################
###################################################################################################

class Words(Base):
    """A class for collecting and analyzing words data for specified terms list(s).

    Attributes
    ----------
    labels : list of str
        Labels for each data object attached to the object.
    has_data : bool
        Whether the object contains data.
    results : list of Articles
        Results of 'Words' data collection for each search term.
    combined_results : list of ArticlesAll
        Results for each search term combined across individual articles.
    meta_data : MetaData
        Meta data information about the data collection.
    """

    def __init__(self):
        """Initialize LISC Words object."""

        Base.__init__(self)

        self.results = list()
        self.combined_results = list()
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


    def __iter__(self):
        """Allow for iterating across the object by stepping through collected results."""

        for result in self.results:
            yield result


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


    def check_articles(self):
        """Prints out the articles collected for each term."""

        for results in self.results:
            print('\nLabel: {}\n'.format(results.label))
            for cres in results:
                author = cres['authors'][0][0] + (' et al' if len(cres['authors']) > 1 else '')
                doi = 'https://dx.doi.org/' + cres['doi'] if cres['doi'] else ''
                print(author + ',', str(cres['year']) + ':', cres['title'], doi)


    def drop_data(self, n_articles):
        """Drop terms based on number of article results.

        Parameters
        ----------
        n_articles : int
            Minimum number of articles required to keep each term.

        Examples
        --------
        Drop terms with less than 20 articles (assuming `words` already has data):

        >>> words.drop_data(20) # doctest: +SKIP
        """

        inds = [ind for ind, res in enumerate(self.results) if res.n_articles < n_articles]

        for ind in list(reversed(sorted(inds))):
            self.drop_term(ind)
            self.results.pop(ind)


    def process_articles(self, process_func=None):
        """Process the articles stored in the object.

        Parameters
        ----------
        process_func : callable, optional
            A function to process article data. Must take as input an `Articles` object.
            If not provided, applies the default `process_articles` function.
        """

        for arts in self.results:
            arts.process(process_func)


    def process_combined_results(self, exclusions=None):
        """Process article data to create combined results, across all articles, for each term.

        Parameters
        ----------
        exclusions : list of str, optional
            Words to exclude from the combined word collections.

        Notes
        -----
        This function will process the article data contained in the object.
        """

        if not self.has_data:
            raise ValueError('Object has no data - cannot proceed.')

        self.combined_results = [ArticlesAll(result, exclusions) for result in self.results]
