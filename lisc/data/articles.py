"""Classes and functions to store and process extracted article data."""

import os
import json

from lisc.data.term import Term
from lisc.utils.db import check_directory
from lisc.data.base_articles import BaseArticles
from lisc.core.errors import InconsistentDataError
from lisc.utils.io import parse_json_data, check_ext

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
    ids : list of int
        Article ids for all articles.
    n_articles : int
        Number of articles collected.
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
    """

    def __init__(self, term):
        """Initialize Articles object.

        Parameters
        ----------
        term : Term or str
            Search term definition. If input is a string, it is used as the label for the term.

        Examples
        --------
        Intialize an ``Articles`` object with a search term:

        >>> articles = Articles('frontal lobe')
        """

        # Inherit from the BaseArticles object
        BaseArticles.__init__(self, term)


    def __iter__(self):
        """Iterate through collected articles."""

        for ind in range(self.n_articles):

            yield {
                'id': self.ids[ind],
                'title': self.titles[ind],
                'journal': self.journals[ind],
                'authors': self.authors[ind],
                'words': self.words[ind],
                'keywords': self.keywords[ind],
                'year': self.years[ind],
                'doi': self.dois[ind]}


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
        Save ``Articles`` data to a temporary directory:

        >>> from tempfile import TemporaryDirectory
        >>> articles = Articles('frontal lobe')
        >>> with TemporaryDirectory() as dirpath:
        ...     articles.save(directory=dirpath)
        """

        directory = check_directory(directory, 'raw')

        with open(os.path.join(directory, check_ext(self.label, '.json')), 'w') as outfile:
            json.dump({'term' : self.term}, outfile)
            outfile.write('\n')
            for art in self:
                json.dump(art, outfile)
                outfile.write('\n')


    def load(self, directory=None):
        """Load raw data from json file.

        Parameters
        ----------
        directory : str or SCDB, optional
            Folder or database object specifying the save location.

        Examples
        --------
        Load ``Articles`` data from a :class:`~.SCDB` folder named 'lisc_db', located in the working
        directory:

        >>> from lisc.utils import SCDB
        >>> articles = Articles('frontal lobe')
        >>> articles.load(SCDB('lisc_db')) # doctest:+SKIP
        """

        directory = check_directory(directory, 'raw')

        data = parse_json_data(os.path.join(directory, check_ext(self.label, '.json')))

        self.term = Term(*next(data)['term'])

        for dat in data:
            self.add_data('ids', dat['id'])
            self.add_data('titles', dat['title'])
            self.add_data('journals', dat['journal'])
            self.add_data('authors', dat['authors'])
            self.add_data('words', dat['words'])
            self.add_data('keywords', dat['keywords'])
            self.add_data('years', dat['year'])
            self.add_data('dois', dat['doi'])

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
