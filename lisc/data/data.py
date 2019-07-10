"""Classes and functions to store and process extracted paper data."""

import json

from lisc.core.db import check_db
from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

class Data():
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
    months : list of int
        Publication month of each article included in object.
    dois : list of str
        DOIs of each article included in object.
    history : list of str
        History of the object and it's data.
    """

    def __init__(self, label, term=[]):
        """Initialize termWords() object.

        Parameters
        ----------
        label : str
            Label for the term.
        term  : list of str
            Name(s) of the term.
        """

        # Set the given name & synonyms as the term label
        self.label = label
        self.term = term

        # Initialize list to store pubmed article ids
        self.ids = list()

        # Initialize to store article count
        self.n_articles = 0

        # Initiliaze to store data pulled from articles
        self.titles = list()
        self.journals = list()
        self.authors = list()
        self.words = list()
        self.kws = list()
        self.years = list()
        self.months = list()
        self.dois = list()

        # Initialize list to track object history
        self.history = list()
        self.update_history('Initialized')


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
                'month': self.months[ind],
                'doi': self.dois[ind]
            }


    def add_id(self, new_id):
        """Add a new ID to termWords object.

        Parameters
        ----------
        new_id : int
            The ID number of the current article.
        """

        self.ids.append(new_id)


    def add_title(self, new_title):
        """Add a new title to termWords object.

        Parameters
        ----------
        new_title : str
            The title of the current article.
        """

        self.titles.append(new_title)


    def add_authors(self, new_authors):
        """Add a new set of authors to termWords object.

        Parameters
        ----------
        new_authors : list of tuple of (str, str, str, str)
            Author list of the current article.
                (LastName, FirstName, Initials, Affiliation)
        """

        self.authors.append(new_authors)


    def add_journal(self, new_journal, new_iso_abbrev):
        """Add a new journal name and ISO abbreviation to termWords object.

        Parameters
        ----------
        new_journal : str
            Name of the journal current article comes from.
        new_iso_abbrev : str
            Standardized abbreviation of journal name article comes from.
        """

        self.journals.append((new_journal, new_iso_abbrev))


    def add_words(self, new_words):
        """Add new words to termWords object.

        Parameters
        ----------
        new_words : list of str
            List of words from the current article.
        """

        self.words.append(new_words)


    def add_kws(self, new_kws):
        """Add new keywords to termWords object.

        Parameters
        ----------
        new_kws : list of str
            List of keywords from current article.
        """

        self.kws.append(new_kws)


    def add_pub_date(self, new_pub_date):
        """Add publication date information to termWords object.

        Parameters
        ----------
        new_pub_date : tuple of (int, str)
            Publication year and month of current article.
        """

        self.years.append(new_pub_date[0])
        self.months.append(new_pub_date[1])


    def add_doi(self, new_doi):
        """Add DOI to termWords object.

        Parameters
        ----------
        new_doi : str
            DOI for the current article.
        """

        self.dois.append(new_doi)


    def increment_n_articles(self):
        """Increment the number of articles included in current object."""

        self.n_articles += 1


    def check_results(self):
        """Check for consistencty in extracted results.

        If everything worked, each data field (ids, titles, words, years)
        should have the same length, equal to the number of articles.
        Some entries may be blank (missing data), but if the lengths are not
        the same then the data does not line up and cannot be trusted.
        """

        # Check that all data fields have length n_articles
        if not (self.n_articles == len(self.ids) == len(self.titles) == len(self.words)
                == len(self.journals) == len(self.authors) == len(self.kws)
                == len(self.years) == len(self.months) == len(self.dois)):

            # If not, print out error
            self.update_history('Failed Check')
            raise InconsistentDataError('term Words data is inconsistent.')

        # Update history
        self.update_history('Passed Check')


    def update_history(self, update):
        """Update object history."""

        self.history.append(update)


    def save(self, db=None):
        """Save out json file with all attached data."""

        db = check_db(db)

        with open(db.words_path + '/raw/' + self.label + '.json', 'w') as outfile:
            for art in self:
                json.dump(art, outfile)
                outfile.write('\n')

        # Update history
        self.update_history('Saved')


    def load(self, db=None):
        """Load raw data from json file."""

        db = check_db(db)

        data = _parse_json_dat(db.words_path + '/raw/' + self.label + '.json')

        for dat in data:
            self.add_id(dat['id'])
            self.add_title(dat['title'])
            self.add_journal(dat['journal'][0], dat['journal'][1])
            self.add_authors(dat['authors'])
            self.add_words(dat['words'])
            self.add_kws(dat['kws'])
            self.add_pub_date([dat['year'], dat['month']])
            self.add_doi(dat['doi'])
            self.increment_n_articles()

        self.check_results()


    def clear(self):
        """Clear all data attached to object."""

        # Re-initiliaze all data lists to be empty
        self.ids = list()
        self.titles = list()
        self.journals = list()
        self.authors = list()
        self.words = list()
        self.kws = list()
        self.years = list()
        self.months = list()
        self.dois = list()

        # Re-initialize article count to zero
        self.n_articles = 0

        # Update history
        self.update_history('Cleared')


    def save_n_clear(self):
        """Save out the attached data and clear the object."""

        self.save()
        self.clear()

###################################################################################################
###################################################################################################

def _parse_json_dat(f_name):
    for l in open(f_name):
        yield json.loads(l)
