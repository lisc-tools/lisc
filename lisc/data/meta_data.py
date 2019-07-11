"""Class to store meta data."""

import datetime

###################################################################################################
###################################################################################################

class MetaData():
    """An object to hold the meta data for a scrape.

    Attributes
    ----------
    date :
        xx
    requester :
        xx
    database_info :
        xx
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
            xx
        """

        requester.close()
        self.requester = requester.as_dict()


    def add_db_info(self, db_info):
        """Add a database information to self.

        Parameters
        ----------
        db_info : dict
            xx
        """

        self.db_info = db_info
