"""Class to store meta data."""

import datetime

###################################################################################################
###################################################################################################

class MetaData():
    """An object to hold the meta data for a scrape.

    Attributes
    ----------
    date : str
        Information on the date that the data collection was run.
    requester : dict
        Information about the requester object used for the scrape.
    database_info : dict
        Information about the database from which the data was accessed.
    """

    def __init__(self):

        self.date = None
        self.requester = None
        self.db_info = None

        self.get_date()


    def __getitem__(self, attr):
        return getattr(self, attr)


    def __repr__(self):
        return str(self.__dict__)


    def get_date(self):
        """Get the current data and attach to object."""

        self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


    def add_requester(self, requester):
        """Add a requester object to self.

        Parameters
        ----------
        requester : Requester() object
            The object used to launch URL requests.
        """

        requester.close()
        self.requester = requester.as_dict()


    def add_db_info(self, db_info):
        """Add a database information to self.

        Parameters
        ----------
        db_info : dict
            Information about the database from which the data was collected.
        """

        self.db_info = db_info
