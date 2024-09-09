"""Load & save functions for LISC."""

import os
import json
import pickle
from pathlib import Path

from lisc.io.db import SCDB, check_directory
from lisc.io.utils import check_ext, get_files, make_folder
from lisc.objects.utils import check_object_type

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

    file_path = check_directory(directory) / check_ext(file_name, '.json')
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

    file_path = check_directory(directory) / check_ext(file_name, '.json')
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

    file_path = check_directory(directory) / check_ext(file_name, '.json')
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

    file_path = check_directory(directory) / check_ext(file_name, '.json')
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

    file_path = check_directory(directory, 'terms') / check_ext(file_name, '.txt')

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

    file_path = check_directory(directory, 'base') / check_ext(file_name, '.txt')

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

    obj_type = check_object_type(obj)
    file_path = check_directory(directory, obj_type) / check_ext(file_name, '.p')

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
            load_path = directory.get_folder_path('counts') / check_ext(file_name, '.p')
        elif check_ext(file_name, '.p') in directory.get_files('words'):
            load_path = directory.get_folder_path('words') / check_ext(file_name, '.p')

    elif isinstance(directory, (str, Path)) or directory is None:

        if file_name in os.listdir(directory):
            directory = '' if directory is None else directory
            load_path = os.path.join(directory, check_ext(file_name, '.p'))

    if not load_path:
        raise ValueError('Can not find requested file name.')

    with open(load_path, 'rb') as load_obj:
        custom_object = pickle.load(load_obj)

    if reload_results:

        for result in custom_object.results:
            result.load(directory=directory)

    return custom_object


def save_time_results(results, folder, file_name, directory=None):
    """Save a set of results collected across time.

    Parameters
    ----------
    results : list of {Counts1D, Counts, Words}
        Results of the collection across time.
    folder : str
        The name of the folder to save the objects to.
    file_name : str
        The name of the file to save each object with.
        Each individual object is saved with this label plus a year marker.
    directory : str or Path
        Location to save to.
    """

    obj_type = check_object_type(results[list(results.keys())[0]])
    folder_path = check_directory(directory, obj_type) / folder
    make_folder(folder_path)

    for key, obj in results.items():
        save_object(obj, file_name + '_' + str(key), folder_path)


def load_time_results(folder, file_name=None, directory=None):
    """Load a set of results collected across time.

    Parameters
    ----------
    folder : str
        Folder to load the results from.
    file_name : str, optional
        A file name to specify a set of files to load.
    directory : str or Path
        Location to load from.
    """

    folder_path = None

    if isinstance(directory, SCDB):

        if folder in directory.get_files('counts'):
            folder_path = check_directory(directory, 'counts') / folder
        elif folder in directory.get_files('words'):
            folder_path = check_directory(directory, 'words') / folder

    elif isinstance(directory, (str, Path)) or directory is None:

        if folder in os.listdir(directory):
            directory = '' if directory is None else directory
            folder_path = os.path.join(directory, folder)

    if not folder_path:
        raise ValueError('Can not find requested folder name.')

    files = get_files(folder_path, select=file_name)

    results = {}
    for file in files:
        year_label = file.split('.')[0].split('_')[-1]
        results[int(year_label)] = load_object(file, folder_path)

    return results


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
