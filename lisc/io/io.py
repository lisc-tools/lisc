"""Load & save functions for LISC."""

import os
import json
import pickle

from lisc.io.db import SCDB, check_directory
from lisc.io.utils import check_ext

###################################################################################################
###################################################################################################

def save_json(data, file_name, directory):
    """Save out a JSON file.

    Parameters
    ----------
    data : dict
        Data to save out to a JSON file.
    file_name : str
        File name to give the saved out json file.
    directory: str or Path, optional
        Folder to save out to.
    """

    file_path = os.path.join(check_directory(directory), check_ext(file_name, '.json'))
    with open(file_path, 'w') as save_file:
        json.dump(data, save_file)


def load_json(file_name, directory):
    """Load from a JSON file.

    Parameters
    ----------
    file_name : str
        File name of the file to load.
    directory : str or Path, optional
        Folder to load from.

    Returns
    -------
    data : dict
        Loaded data from the JSON file.
    """

    file_path = os.path.join(check_directory(directory), check_ext(file_name, '.json'))
    with open(file_path) as json_file:
        data = json.load(json_file)

    return data


def save_jsonlines(data, file_name, directory=None, header=None):
    """Save out data to a JSONlines file.

    Parameters
    ----------
    data : list of dict or iterable
        Data to save out to a JSONlines file.
    file_name : str
        File name to give the saved out json file.
    directory : str or Path, optional
        Folder to save out to.
    header : dict, optional
        Data to save out as the header line of the file.
    """

    file_path = os.path.join(check_directory(directory), check_ext(file_name, '.json'))
    with open(file_path, 'w') as outfile:
        if header:
            json.dump(header, outfile)
            outfile.write('\n')
        for cdata in data:
            json.dump(cdata, outfile)
            outfile.write('\n')


def parse_json_data(file_name, directory=None):
    """Parse data from a json file.

    Parameters
    ----------
    file_name : str
        File name of the json file.
    directory : str or Path, optional
        Folder or database object specifying the location to load the file from.

    Yields
    ------
    str
        The loaded line of json data.
    """

    file_path = os.path.join(check_directory(directory), check_ext(file_name, '.json'))
    with open(file_path) as f_obj:
        for line in f_obj:
            yield json.loads(line)


def load_txt_file(file_name, directory=None, split_elements=True, split_character=','):
    """Load contents from a text file.

    Parameters
    ----------
    file_name : str
        Name of the file to load.
    directory : str or Path or SCDB, optional
        Folder or database object specifying the location of the file to load.
    split_elements : bool, optional, default: True
        If True, splits elements within a single line.
    split_character : str, optional, default: ','
        The character to use to split elements within a line.

    Returns
    -------
    contents : list
        Data loaded from the file.
    """

    file_path = os.path.join(check_directory(directory, 'terms'), check_ext(file_name, '.txt'))

    with open(file_path, 'r') as terms_file:

        text = terms_file.read()

        # If the last line is empty, it gets cut off due to no trailing content
        #   To make sure there is the correct number of lines, add a newline character
        if text.endswith('\n'):
            text = text + '\n'

        contents = text.splitlines()

    if split_elements:
        contents = [line.split(split_character) for line in contents]
        contents = [[string.strip() for string in temp] for temp in contents]

    else:
        contents = [string.strip() for string in contents]

    return contents


def load_api_key(file_name, directory=None, required=False):
    """Load an API key from a file.

    Parameters
    ----------
    file_name : str
        Name of the file to load.
    directory : str or Path or SCDB, optional
        Folder or database object specifying the location of the file to load.
    required : bool, optional, default: False
        Whether loading the API key file is required for continued execution.
        If True, this function will raise an error if the requested file is not found.
        If False, this function will return None if the file is not found.

    Returns
    -------
    api_key : str or None
        The loaded API key.

    Raises
    ------
    FileNotFoundError
        If the requested file. Only raised if `required` is True.

    Notes
    -----
    This function assumes the API key is in a single-line txt file.
    """

    file_path = os.path.join(check_directory(directory, 'base'), check_ext(file_name, '.txt'))

    try:

        with open(file_path, 'r') as f_obj:
            api_key = f_obj.read().strip()

    except Exception as error:

        if required:
            raise
        else:
            api_key = None

    return api_key


def save_object(obj, file_name, directory=None):
    """Save a custom object as a pickle file.

    Parameters
    ----------
    obj : Counts or Words
        Object to save out.
    file_name : str
        Name for the file to be saved out.
    directory : str or Path or SCDB, optional
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
    from lisc.objects import Counts1D, Counts, Words

    # Set the save path based on object type
    if isinstance(obj, (Counts1D, Counts)):
        obj_type = 'counts'
    elif isinstance(obj, Words):
        obj_type = 'words'
    else:
        raise ValueError('Object type unclear - can not save.')

    file_path = os.path.join(check_directory(directory, obj_type), check_ext(file_name, '.p'))

    with open(file_path, 'wb') as file_path:
        pickle.dump(obj, file_path)


def load_object(file_name, directory=None, reload_results=False):
    """Load a custom object, from a pickle file.

    Parameters
    ----------
    file_name : str
        File name of the object to be loaded.
    directory : str or Path or SCDB, optional
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

    load_path = check_ext(load_path, '.p')

    with open(load_path, 'rb') as load_obj:
        custom_object = pickle.load(load_obj)

    if reload_results:

        for result in custom_object.results:
            result.load(directory=directory)

    return custom_object


def save_meta_data(meta_data, file_name, directory):
    """Save out a meta object, as a JSON file.

    Parameters
    ----------
    meta_data : MetaData
        Object containing metadata.
    file_name : str
        Name of the file to save to.
    directory : str or Path or SCDB, optional
        Folder or database object specifying the location to save the file.
    """

    save_json(meta_data.as_dict(), file_name, check_directory(directory, 'logs'))


def load_meta_data(file_name, directory=None):
    """Load a MetaData object from file.

    Parameters
    ----------
    file_name : str
        Name of the file to load.
    directory : str or Path or SCDB, optional
        Folder or database object specifying the location to load the file from.

    Returns
    -------
    meta_data : MetaData
        Object containing metadata.
    """

    # Import objects locally, to avoid circular imports
    from lisc.data.meta_data import MetaData

    meta_dict = load_json(file_name, check_directory(directory, 'logs'))

    meta_data = MetaData()
    meta_data.from_dict(meta_dict)

    return meta_data
