"""Base classes store and process extracted paper data."""

from lisc.data.term import Term

###################################################################################################
###################################################################################################

class BaseData():
    """Base object for storing collected article data."""

    def __init__(self, term):
        """Initialize BaseData object.

        Parameters
        ----------
        term : Term() object or str
            Search term definition.
            If input is a string, it is used as the label for the term.
        """

        # If term provided is a string, consider it the label and make a Term object
        if isinstance(term, str):
            term = Term(term, [], [], [])

        self.term = term

        self.ids = list()
        self.titles = list()
        self.journals = list()
        self.authors = list()
        self.words = list()
        self.kws = list()
        self.years = list()
        self.dois = list()

    @property
    def label(self):
        return self.term.label

    @property
    def n_articles(self):
        return len(self.ids)


    def clear(self):
        """Clear all data attached to object."""

        self.ids = list()
        self.titles = list()
        self.journals = list()
        self.authors = list()
        self.words = list()
        self.kws = list()
        self.years = list()
        self.dois = list()
