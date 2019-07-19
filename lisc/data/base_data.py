"""Base classes store and process extracted paper data."""

###################################################################################################
###################################################################################################

class BaseData():
    """Base object for storing collected article data."""

    def __init__(self, term):

        self.term = term

        # Initialize list to store pubmed article ids
        self.ids = list()

        # Initiliaze to store data pulled from articles
        self.titles = list()
        self.journals = list()
        self.authors = list()
        self.words = list()
        self.kws = list()
        self.years = list()
        self.dois = list()

        # Initialize list to track object history
        self.history = list()
        self.update_history('Initialized')

    @property
    def label(self):
        return self.term
    #    return self.term['term'][0]

    @property
    def n_articles(self):
        return len(self.ids)


    def update_history(self, update):
        """Update object history.

        Parameters
        ----------
        update : str
            A message to add to the history.
        """

        self.history.append(update)


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

        self.update_history('Cleared')
