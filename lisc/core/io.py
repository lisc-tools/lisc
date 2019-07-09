"""Load & save functions for LISC."""

import os
import pickle

from lisc.words import Words
from lisc.count import Count
from lisc.core.db import check_db
from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

def save_object(obj, f_name, db=None):
    """Save a custom object from LISC as a pickle file.

    Parameters
    ----------
    obj : Counts() or Words() object
        LISC custom object to save out.
    f_name : str
        Name to append to saved out file name.
    db : SCDB() object, optional
        Database object for the LISC project.
    """

    # Check for database object, initialize if not provided
    db = check_db(db)

    # Set the save path based on object type
    if isinstance(obj, Count):
        save_path = db.counts_path
    elif isinstance(obj, Words):
        save_path = db.words_path
    else:
        raise InconsistentDataError('Object type unclear - can not save.')

    pickle.dump(obj, open(os.path.join(save_path, save_name), 'wb'))


def load_object(f_name, db=None):
    """Load a custom object, from a pickle file.

    Parameters
    ----------
    f_name : str
        File name of the object to be loaded.
    db : SCDB object, optional
        Database object for the SCANR project.

    Returns
    -------
    object
        Custom object loaded from pickle file.
    """

    # Check for database object, initialize if not provided
    db = check_db(db)

    # Get all available files, for Count and Words pickled objects
    counts_objs = os.listdir(db.counts_path)
    words_objs = os.listdir(db.words_path)

    # Search for object in saved Count files, and set path if found
    if f_name + '.p' in counts_objs:
        load_path = os.path.join(db.counts_path, f_name + '.p')

    # Search for object in saved Words files, and set path if found
    elif f_name + '.p' in words_objs:
        load_path = os.path.join(db.words_path, f_name + '.p')

    # Raise an error if the file name is not found
    else:
        raise InconsistentDataError('Can not find requested file name.')

    return pickle.load(open(load_path, 'rb'))
