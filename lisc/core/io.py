"""Load & save functions for LISC."""

import os
import json
import pickle

from lisc.core.db import SCDB, check_folder
from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

def check_ext(f_name, ext):
    """Check the extension for a file name, and add if missing.

    Parameters
    ----------
    f_name : str
        The name of the file.
    ext : str
        The extension to check and add.

    Returns
    -------
    str
        File name with the extenion added.
    """

    return f_name + ext if not f_name.endswith(ext) else f_name


def load_terms_file(f_name, folder=None):
    """Loads terms from a text file.

    Parameters
    ----------
    f_name : str
        Name of the file to load.
    folder : str or SCDB() object, optional
        Folder or database object specifying the save location.

    Returns
    -------
    dat : list of str
        Data from the file.
    """

    terms_file = open(os.path.join(check_folder(folder, 'terms'),
                                   check_ext(f_name, '.txt')), 'r')
    dat = terms_file.read().splitlines()

    return dat


def save_object(obj, f_name, folder=None):
    """Save a custom object from LISC as a pickle file.

    Parameters
    ----------
    obj : Counts() or Words() object
        LISC custom object to save out.
    f_name : str
        Name for the file to be saved out.
    folder : str or SCDB() object, optional
        Folder or database object specifying the save location.
    """

    # Set the save path based on object type
    # Note: imports done here to stop circular imports
    from lisc.objects import Counts, Words
    if isinstance(obj, Counts):
        obj_type = 'counts'
    elif isinstance(obj, Words):
        obj_type = 'words'
    else:
        raise InconsistentDataError('Object type unclear - can not save.')

    pickle.dump(obj, open(os.path.join(check_folder(folder, obj_type),
                                       check_ext(f_name, '.p')), 'wb'))


def load_object(f_name, folder=None):
    """Load a custom object, from a pickle file.

    Parameters
    ----------
    f_name : str
        File name of the object to be loaded.
    folder : str or SCDB() object, optional
        Folder or database object specifying the save location.

    Returns
    -------
    object
        Custom object loaded from pickle file.
    """

    load_path = None

    if isinstance(folder, SCDB):

        if check_ext(f_name, '.p') in folder.get_files('counts'):
            load_path = os.path.join(folder.counts_path, f_name)
        elif check_ext(f_name, '.p') in folder.get_files('words'):
            load_path = os.path.join(folder.words_path, f_name)

    elif isinstance(folder, str) or folder is None:

        if f_name in os.listdir(folder):
            load_path = os.path.join(folder, f_name)

    if not load_path:
        raise InconsistentDataError('Can not find requested file name.')

    return pickle.load(open(check_ext(load_path, '.p'), 'rb'))


def parse_json_data(f_name):
    """Parse data from a json file.

    Parameters
    ----------
    f_name : str
        File name of the json file to be loaded.

    Yields
    ------
    str
        The loaded line of json data.
    """

    for line in open(f_name):
        yield json.loads(line)
