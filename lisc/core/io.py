"""Load & save functions for SCANR."""

import os
import pickle

from lisc.words import Words
from lisc.count import Count
from lisc.core.db import check_db
from lisc.core.errors import InconsistentDataError

##########################################################################################
##########################################################################################
##########################################################################################

def save_pickle_obj(obj, f_name, db=None):
    """Save a custom object from LISC as a pickle file.

    Parameters
    ----------
    obj : {Counts() object, Words() object}
        LISC custom object to save out.
    f_name : str
        Name to append to saved out file name.
    db : SCDB() object, optional
        Database object for the LISC project.
    """

    # Check for database object, initialize if not provided
    db = check_db(db)

    # If it's a Counts object, set path and name
    if isinstance(obj, Count):
        save_name = f_name + '_counts.p'
        save_path = db.counts_path

    # If it's a Words object, set path and name
    elif isinstance(obj, Words):
        save_name = f_name + '_words.p'
        save_path = db.words_path

    # If neither, raise error as object type is unclear
    else:
        raise InconsistentDataError('Object type unclear - can not save.')

    # Save out labels header file
    #with open(os.path.join(save_path, 'labels.txt'), 'w') as outfile:
    #    for label in obj.labels:
    #        outfile.write("%s\n" % label)

    # Save pickle file
    save_file = os.path.join(save_path, save_name)
    pickle.dump(obj, open(save_file, 'wb'))


def load_pickle_obj(f_name, db=None):
    """Load a custom object, from a pickle file, for SCANR project.

    Parameters
    ----------
    f_name : str
        File name of the object to be loaded.
    db : SCDB object, optional
        Database object for the SCANR project.
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

    # Load and return the data
    return pickle.load(open(load_path, 'rb'))
