"""Load & save functions for LISC."""

import os
import json
import pickle

from lisc.utils.db import SCDB, check_directory

###################################################################################################
###################################################################################################

def check_ext(file_name, ext):
    """Check the extension for a file name, and add if missing.

    Parameters
    ----------
    file_name : str
        The name of the file.
    ext : str
        The extension to check and add.

    Returns
    -------
    str
        File name with the extension added.
    """

    return file_name + ext if not file_name.endswith(ext) else file_name


def load_terms_file(file_name, directory=None):
    """Loads terms from a text file.

    Parameters
    ----------
    file_name : str
        Name of the file to load.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.

    Returns
    -------
    terms : list of list of str
        Data from the file.
    """

    terms_file = open(os.path.join(check_directory(directory, 'terms'),
                                   check_ext(file_name, '.txt')), 'r')
    terms = terms_file.read().splitlines()
    terms = [term.split(',') for term in terms]

    return terms


def save_object(obj, file_name, directory=None):
    """Save a custom object as a pickle file.

    Parameters
    ----------
    obj : Counts or Words
        Object to save out.
    file_name : str
        Name for the file to be saved out.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.

    Examples
    --------
    Save a :class:`~.Counts` object, using a temporary directory:

    >>> from tempfile import TemporaryDirectory
    >>> from lisc.objects import Counts
    >>> with TemporaryDirectory() as dirpath:
    ...     save_object(Counts(), 'counts.p', directory=dirpath)
    """

    # Import objects locally, to avoid circular imports
    from lisc.objects import Counts, Words

    # Set the save path based on object type
    if isinstance(obj, Counts):
        obj_type = 'counts'
    elif isinstance(obj, Words):
        obj_type = 'words'
    else:
        raise ValueError('Object type unclear - can not save.')

    pickle.dump(obj, open(os.path.join(check_directory(directory, obj_type),
                                       check_ext(file_name, '.p')), 'wb'))


def load_object(file_name, directory=None, reload_results=False):
    """Load a custom object, from a pickle file.

    Parameters
    ----------
    file_name : str
        File name of the object to be loaded.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.

    Returns
    -------
    custom_object
        Custom object loaded from pickle file.

    Examples
    --------
    Load a :class:`~.Counts` object, using a temporary directory:

    >>> from tempfile import TemporaryDirectory
    >>> from lisc.objects import Counts
    >>> with TemporaryDirectory() as dirpath:
    ...     save_object(Counts(), 'counts.p', directory=dirpath)
    ...     counts = load_object('counts.p', directory=dirpath)
    """

    load_path = None

    if isinstance(directory, SCDB):

        if check_ext(file_name, '.p') in directory.get_files('counts'):
            load_path = os.path.join(directory.get_folder_path('counts'), file_name)
        elif check_ext(file_name, '.p') in directory.get_files('words'):
            load_path = os.path.join(directory.get_folder_path('words'), file_name)

    elif isinstance(directory, str) or directory is None:

        if file_name in os.listdir(directory):
            directory = '' if directory is None else directory
            load_path = os.path.join(directory, file_name)

    if not load_path:
        raise ValueError('Can not find requested file name.')

    custom_object = pickle.load(open(check_ext(load_path, '.p'), 'rb'))

    if reload_results:

        for result in custom_object.results:
            result.load(directory=directory)

    return custom_object


def parse_json_data(file_name):
    """Parse data from a json file.

    Parameters
    ----------
    file_name : str
        File name of the json file.

    Yields
    ------
    str
        The loaded line of json data.
    """

    for line in open(file_name):
        yield json.loads(line)
