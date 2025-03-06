"""Classes and functions to store and process extracted article data."""

from lisc.data.term import Term
from lisc.data.process import process_articles
from lisc.data.base_articles import BaseArticles
from lisc.modutils.errors import InconsistentDataError, ProcessingError
from lisc.io.db import check_directory
from lisc.io.io import save_jsonlines, parse_json_data

###################################################################################################
###################################################################################################

class Articles(BaseArticles):
    """An object to hold collected 'words' data for a specified term.

    Attributes
    ----------
    label : str
        Label for the term.
    term : Term
        Definition of the search term, with inclusion and exclusion words.
    has_data : bool
        Whether the object contains data.
    n_articles : int
        Number of articles collected.
    ids : list of int
        Article ids for all articles.
    titles : list of str
        Titles of all articles.
    journals : list of tuple of (str, str)
        Journals that the articles come from, as (Journal Name, ISO abbreviation).
    authors : list of list of str
        Authors of all articles, as (Last Name, First Name, Initials, Affiliation).
    words : list of list of str
        Words extracted from the abstract of each article.
    keywords : list of list of str
        Keywords from each article.
    years : list of int
        Publication year of each article.
    dois : list of str
        DOIs of each article.
    processed : bool
        Whether the article data has been processed.
    """

    def __init__(self, term):
        """Initialize Articles object.

        Parameters
        ----------
        term : Term or str
            Search term definition. If input is a string, it is used as the label for the term.

        Examples
        --------
        Initialize an ``Articles`` object, with a label for the search term it represents:

        >>> articles = Articles('frontal lobe')
        """

        # Inherit from the BaseArticles object
        BaseArticles.__init__(self, term)
        self.processed = False


    def __getitem__(self, ind):
        """Index into a object, getting a specific article based on it's index."""

        if len(self) == 0:
            raise IndexError('No data is available - cannot proceed.')

        return {'id': self.ids[ind],
                'title': self.titles[ind],
                'journal': self.journals[ind],
                'authors': self.authors[ind],
                'words': self.words[ind],
                'keywords': self.keywords[ind],
                'year': self.years[ind],
                'doi': self.dois[ind]}


    def __iter__(self):
        """Iterate through collected articles."""

        for ind in range(self.n_articles):
            yield self[ind]


    def __len__(self):
        """Add access to getting length of object as number of articles."""

        return self.n_articles


    def add_data(self, field, new_data):
        """Add data to object.

        Parameters
        ----------
        field : str
            The attribute of the object to add data to.
        new_data : str or int or list
            Data to add to object.

        Examples
        --------
        Add a journal to an ``Articles`` object:

        >>> articles = Articles('frontal lobe')
        >>> articles.add_data('journals', 'Nature')
        """

        getattr(self, field).append(new_data)


    def save(self, directory=None):
        """Save out a json file with all attached data.

        Parameters
        ----------
        directory : str or SCDB, optional
            Folder or database object specifying the save location.

        Examples
        --------
        Save an ``Articles`` object, using a temporary directory:

        >>> from tempfile import TemporaryDirectory
        >>> articles = Articles('frontal lobe')
        >>> with TemporaryDirectory() as dirpath:
        ...     articles.save(directory=dirpath)
        """

        save_jsonlines(self, self.label, check_directory(directory, 'raw'),
                       header={'term' : self.term})


    def load(self, directory=None):
        """Load raw data from json file.

        Parameters
        ----------
        directory : str or SCDB, optional
            Folder or database object specifying the save location.

        Examples
        --------
        Load an ``Articles`` object, assuming an :class:`~.SCDB` organization named 'lisc_db':

        >>> from lisc.utils import SCDB
        >>> articles = Articles('frontal lobe')
        >>> articles.load(SCDB('lisc_db')) # doctest:+SKIP
        """

        data = parse_json_data(self.label, check_directory(directory, 'raw'))

        self.term = Term(*next(data)['term'])

        for datum in data:
            self.add_data('ids', datum['id'])
            self.add_data('titles', datum['title'])
            self.add_data('journals', datum['journal'])
            self.add_data('authors', datum['authors'])
            self.add_data('words', datum['words'])
            self.add_data('keywords', datum['keywords'])
            self.add_data('years', datum['year'])
            self.add_data('dois', datum['doi'])

        self._check_results()


    def save_and_clear(self, directory=None):
        """Save out the attached data and clear the object.

        Parameters
        ----------
        directory : str or SCDB, optional
            Folder or database object specifying the save location.

        Examples
        --------
        Save and clear data from an ``Articles`` object:

        >>> from tempfile import TemporaryDirectory
        >>> articles = Articles('frontal lobe')
        >>> with TemporaryDirectory() as dirpath:
        ...     articles.save_and_clear(directory=dirpath)
        """

        self.save(directory)
        self.clear()


    def process(self, process_func=None):
        """Process the data stored in the current object.

        Parameters
        ----------
        process_func : callable, optional
            A function to process the articles. Must take as input an `Articles` object.
            If not provided, applies the default `process_articles` function.
        """

        if self.processed:
            raise ProcessingError('Articles have already been processed - cannot process again.')

        if not process_func:
            process_func = process_articles

        process_func(self)
        self.processed = True


    def _check_results(self):
        """Check for consistency in extracted results.

        Notes
        -----
        If everything worked, each data field (ids, titles, words, etc)
        should have the same length, equal to the number of articles.
        Some entries may be blank (missing data), but if the lengths are not
        the same then the data does not line up and something went wrong.
        """

        # Check that all data fields have length n_articles
        if not (self.n_articles == len(self.ids) == len(self.titles)
                == len(self.words) == len(self.journals) == len(self.authors)
                == len(self.keywords) == len(self.years) == len(self.dois)):

            raise InconsistentDataError('Words data is inconsistent.')
