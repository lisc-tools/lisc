"""Load & save functions for LISC."""

import os
import json
import pickle

from lisc.utils.db import SCDB, check_directory

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
        File name with the extension added.
    """

    return f_name + ext if not f_name.endswith(ext) else f_name


def load_terms_file(f_name, directory=None):
    """Loads terms from a text file.

    Parameters
    ----------
    f_name : str
        Name of the file to load.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.

    Returns
    -------
    terms : list of list of str
        Data from the file.

    Examples
    --------
    Load a ``Counts`` object from a SCANR database saved in a folder named 'lisc_db':

    >>> from tempfile import TemporaryDirectory
    >>> from lisc.utils import SCDB
    >>> counts = load_object('tutorial_counts', directory=SCDB('lisc_db')) # doctest:+SKIP
    """

    terms_file = open(os.path.join(check_directory(directory, 'terms'),
                                   check_ext(f_name, '.txt')), 'r')
    terms = terms_file.read().splitlines()
    terms = [term.split(',') for term in terms]

    return terms


def save_object(obj, f_name, directory=None):
    """Save a custom object as a pickle file.

    Parameters
    ----------
    obj : Counts or Words
        Object to save out.
    f_name : str
        Name for the file to be saved out.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.

    Examples
    --------
    Save a ``Counts`` object:

    >>> from tempfile import TemporaryDirectory
    >>> from lisc.objects import Counts
    >>> with TemporaryDirectory() as dirpath:
    ...     save_object(Counts(), 'counts.p', directory=dirpath)
    """

    # Set the save path based on object type
    # Note: imports done here to stop circular imports
    from lisc.objects import Counts, Words
    if isinstance(obj, Counts):
        obj_type = 'counts'
    elif isinstance(obj, Words):
        obj_type = 'words'
    else:
        raise ValueError('Object type unclear - can not save.')

    pickle.dump(obj, open(os.path.join(check_directory(directory, obj_type),
                                       check_ext(f_name, '.p')), 'wb'))


def load_object(f_name, directory=None):
    """Load a custom object, from a pickle file.

    Parameters
    ----------
    f_name : str
        File name of the object to be loaded.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.

    Returns
    -------
    object
        Custom object loaded from pickle file.

    Examples
    --------
    Load a :class:`~.Counts` object:

    >>> from tempfile import TemporaryDirectory
    >>> from lisc.objects import Counts
    >>> with TemporaryDirectory() as dirpath:
    ...     save_object(Counts(), 'counts.p', directory=dirpath)
    ...     counts = load_object('counts.p', directory=dirpath)
    """

    load_path = None

    if isinstance(directory, SCDB):

        if check_ext(f_name, '.p') in directory.get_files('counts'):
            load_path = os.path.join(directory.get_folder_path('counts'), f_name)
        elif check_ext(f_name, '.p') in directory.get_files('words'):
            load_path = os.path.join(directory.get_folder_path('words'), f_name)

    elif isinstance(directory, str) or directory is None:

        if f_name in os.listdir(directory):
            load_path = os.path.join(directory, f_name)

    if not load_path:
        raise ValueError('Can not find requested file name.')

    return pickle.load(open(check_ext(load_path, '.p'), 'rb'))


def parse_json_data(f_name):
    """Parse data from a json file.

    Parameters
    ----------
    f_name : str
        File name of the json file.

    Yields
    ------
    str
        The loaded line of json data.
    """

    for line in open(f_name):
        yield json.loads(line)
