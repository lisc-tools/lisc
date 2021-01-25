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
        Folder or database object specifying the location of the file to load.

    Returns
    -------
    terms : list of list of str
        Data from the file.
    """

    file_path = os.path.join(check_directory(directory, 'terms'), check_ext(f_name, '.txt'))

    with open(file_path, 'r') as terms_file:
        text = terms_file.read()

        # If the last line is empty, it gets cut off due to no trailing content
        #   To make sure there is the correct number of lines, add a newline character
        if text.endswith('\n'):
            text = text + '\n'

        lines = text.splitlines()

    terms = [term.split(',') for term in lines]

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

    file_path = os.path.join(check_directory(directory, obj_type), check_ext(f_name, '.p'))

    with open(file_path, 'wb') as file_path:
        pickle.dump(obj, file_path)


def load_object(f_name, directory=None, reload_results=False):
    """Load a custom object, from a pickle file.

    Parameters
    ----------
    f_name : str
        File name of the object to be loaded.
    directory : str or SCDB, optional
        Folder or database object specifying the location to load from.
    reload_results : bool, optional, default: False
        Whether to reload individual results into the loaded object.
        Only applies if loading a Words object.

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

        if check_ext(f_name, '.p') in directory.get_files('counts'):
            load_path = os.path.join(directory.get_folder_path('counts'), f_name)
        elif check_ext(f_name, '.p') in directory.get_files('words'):
            load_path = os.path.join(directory.get_folder_path('words'), f_name)

    elif isinstance(directory, str) or directory is None:

        if f_name in os.listdir(directory):
            directory = '' if directory is None else directory
            load_path = os.path.join(directory, f_name)

    if not load_path:
        raise ValueError('Can not find requested file name.')

    load_path = check_ext(load_path, '.p')

    with open(load_path, 'rb') as load_obj:
        custom_object = pickle.load(load_obj)

    if reload_results:

        for result in custom_object.results:
            result.load(directory=directory)

    return custom_object


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

    with open(f_name) as f_obj:
        for line in f_obj:
            yield json.loads(line)
