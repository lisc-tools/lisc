"""Base classes store and process collected article data."""

from lisc.data.term import Term

###################################################################################################
###################################################################################################

class BaseArticles():
    """Base object for storing collected article data."""

    def __init__(self, term):
        """Initialize BaseData object.

        Parameters
        ----------
        term : Term or str
            Search term definition. If input is a string, it is used as the label for the term.
        """

        # If term provided is a string, consider it the label and make a Term object
        if isinstance(term, str):
            term = Term(term, [], [], [])
        self.term = term

        # Initialize the data attributes
        self._initialize_attributes()


    def _initialize_attributes(self):
        """Initialize the data attributes of the object."""

        self.ids = list()
        self.titles = list()
        self.journals = list()
        self.authors = list()
        self.words = list()
        self.keywords = list()
        self.years = list()
        self.dois = list()


    @property
    def label(self):
        """The label for the current term."""

        return self.term.label


    @property
    def has_data(self):
        """Whether the current object contains data."""

        return bool(self.n_articles)


    @property
    def n_articles(self):
        """The number of articles included in the object."""

        return len(self.ids)


    def clear(self):
        """Clear all data attached to object."""

        # Clear attributes by re-initializing to empty
        self._initialize_attributes()
