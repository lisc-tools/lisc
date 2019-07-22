"""Base classes store and process extracted paper data."""

###################################################################################################
###################################################################################################

class BaseData():
    """Base object for storing collected article data."""

    def __init__(self, term):

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
