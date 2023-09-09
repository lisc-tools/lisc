"""Class to store meta data."""

from copy import deepcopy
from datetime import datetime

from lisc.requester import Requester

###################################################################################################
###################################################################################################

class MetaData():
    """An object to hold the meta data for data collection.

    Attributes
    ----------
    date : str
        The date that the data collection was run.
    requester : dict
        Details of the requester object used for the data collection.
    db_info : dict
        Details of the database from which the data was accessed.
    settings : dict
        Details of any search settings that were used during the collection.
    log : list or None
        A log of requested URLs, if requests were logged.
    """

    def __init__(self):
        """Initialize a MetaData object."""

        self.date = None
        self.requester = None
        self.db_info = None
        self.settings = None
        self.log = None

        self.get_date()

        # Add information about which attributes are themselves dictionaries, etc
        self._dict_attrs = ['requester', 'db_info', 'settings']
        self._flat_attrs = ['date', 'log']


    def __getitem__(self, attr):
        return getattr(self, attr)


    def __repr__(self):
        return str(self.as_dict())


    def as_dict(self):
        """Get the attributes of the MetaData object as a dictionary."""

        # Copy so attributes aren't dropped from object itself; drop hidden attributes & unpack
        meta_dict = deepcopy(self.__dict__)
        meta_dict = {key : val for key, val in meta_dict.items() if key[0] != '_'}
        meta_dict = self._unpack_dict(meta_dict)

        return meta_dict


    def get_date(self):
        """Get the current data and attach to object."""

        self.date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


    def add_requester(self, requester, close=True):
        """Add a requester to the MetaData object.

        Parameters
        ----------
        requester : Requester or dict
            If Requester, the object used to launch URL requests.
            If dict, information from a requester object.
        close : bool, optional, default: True
            Whether to close the requester.
        """

        if isinstance(requester, Requester):
            if close:
                requester.close()
            requester = requester.as_dict()

        _ = requester.pop('is_active', None)
        log = requester.pop('log', None)
        if isinstance(log, list):
            self.log = log

        self.requester = requester


    def add_db_info(self, db_info):
        """Add database information to the MetaData object.

        Parameters
        ----------
        db_info : dict
            Information about the database from which the data was collected.
        """

        self.db_info = db_info


    def add_settings(self, settings):
        """Add search settings information to the MetaData object.

        Parameters
        ----------
        settings : dict
            Information about settings that were used during the data collection.
        """

        self.settings = settings


    def from_dict(self, meta_dict):
        """Populate object from an input dictionary.

        Parameters
        ----------
        meta_dict : dict
            Dictionary of information to add to the object.
        """

        if self._dict_attrs[0] not in meta_dict.keys():
            meta_dict = self._repack_dict(meta_dict)

        for label in self._flat_attrs:
            setattr(self, label, meta_dict[label])

        for label in self._dict_attrs:
            if meta_dict[label]:
                getattr(self, 'add_' + label)(meta_dict[label])


    def _unpack_dict(self, meta_dict):
        """Unpack dictionary representation attributes to create a flattened dictionary."""

        for label in self._dict_attrs:
            attr = meta_dict.pop(label)
            if attr:
                for key, val in attr.items():
                    meta_dict[label + '_' + key] = val

        return meta_dict


    def _repack_dict(self, meta_dict):
        """Repack dictionary representation attributes to create a hierarchical dictionary."""

        new_meta_dict = {}
        for label in self._dict_attrs:
            new_meta_dict[label] = {}
            for key, value in meta_dict.items():
                if label in key:
                    new_meta_dict[label][key[len(label)+1:]] = value
        for label in self._flat_attrs:
            new_meta_dict[label] = meta_dict[label]

        return new_meta_dict
