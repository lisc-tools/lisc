"""Classes and functions to store and process extracted paper data."""

import os
import json

from lisc.core.db import check_folder
from lisc.core.io import parse_json_data, check_ext
from lisc.core.errors import InconsistentDataError
from lisc.data.base_data import BaseData

###################################################################################################
###################################################################################################

class Data(BaseData):
    """An object to hold the word results for a given term or term.

    Attributes
    ----------
    label : str
        Label for the current term.
    term : list of str
        Name(s) of the term word data relates to (search terms).
    ids : list of int
        Pubmed article ids for all articles included in object.
    n_articles : int
        Number of articles included in object.
    titles : list of str
        Titles of all articles included in object.
    journals : list of tuple of (str, str)
        List of journals articles come from.
        (Journal Name, ISO abbreviation).
    authors : list of list of str
        Authors of all articles included in object.
        (Last Name, First Name, Initials, Affiliation)
    words : list of list of unicode
        Words extracted from each article.
    kws : list of list of str
        List of keywords for each article included in the object.
    years : list of int
        Publication year of each article included in object.
    dois : list of str
        DOIs of each article included in object.
    """

    def __init__(self, term):
        """Initialize Data() object.

        Parameters
        ----------
        term  : Term() object
            Search term definition
        """

        # Inherit from the BaseData object
        BaseData.__init__(self, term)


    def __iter__(self):
        """Iterate through extracted term papers."""

        for ind in range(self.n_articles):

            yield {
                'label': self.label,
                'term': self.term,
                'id': self.ids[ind],
                'title': self.titles[ind],
                'journal': self.journals[ind],
                'authors': self.authors[ind],
                'words': self.words[ind],
                'kws': self.kws[ind],
                'year': self.years[ind],
                'doi': self.dois[ind]
            }


    def add_data(self, field, new_data):
        """Add data to object.

        Parameters
        ----------
        field : str
            xx
        new_data : str or int or list
            xx
        """

        getattr(self, field).append(new_data)


    def check_results(self):
        """Check for consistencty in extracted results.

        If everything worked, each data field (ids, titles, words, years)
        should have the same length, equal to the number of articles.
        Some entries may be blank (missing data), but if the lengths are not
        the same then the data does not line up and cannot be trusted.
        """

        # Check that all data fields have length n_articles
        if not (self.n_articles == len(self.ids) == len(self.titles)
                == len(self.words) == len(self.journals) == len(self.authors)
                == len(self.kws) == len(self.years) == len(self.dois)):

            raise InconsistentDataError('Words data is inconsistent.')


    def save(self, folder=None):
        """Save out json file with all attached data.

        Parameters
        ----------
        folder : str or SCDB() object, optional
            Folder or database object specifying the save location.
        """

        folder = check_folder(folder, 'raw')

        with open(os.path.join(folder, check_ext(self.label, '.json')), 'w') as outfile:
            for art in self:
                json.dump(art, outfile)
                outfile.write('\n')


    def load(self, folder=None):
        """Load raw data from json file.

        Parameters
        ----------
        folder : str or SCDB() object, optional
            Folder or database object specifying the save location.
        """

        folder = check_folder(folder, 'raw')

        data = parse_json_data(os.path.join(folder, check_ext(self.label, '.json')))

        for dat in data:
            self.add_data('ids', dat['id'])
            self.add_data('titles', dat['title'])
            self.add_data('journals', dat['journal'])
            self.add_data('authors', dat['authors'])
            self.add_data('words', dat['words'])
            self.add_data('kws', dat['kws'])
            self.add_data('years', dat['year'])
            self.add_data('dois', dat['doi'])

        self.check_results()


    def save_n_clear(self, folder=None):
        """Save out the attached data and clear the object.

        Parameters
        ----------
        folder : str or SCDB() object, optional
            Folder or database object specifying the save location.
        """

        self.save(folder)
        self.clear()
