"""File utility function functions."""

import os

###################################################################################################
###################################################################################################

def get_files(folder, drop_ext=False, sort_files=True, drop_hidden=True, select=None):
    """Get a list of files from a directory.

    Parameters
    ----------
    folder : str or Path
        Name of the folder to get the list of files from.
    drop_ext : bool, optional, default: False
        Whether the drop the file extensions from the returned file list.
    sort_files : bool, optional, default: True
        Whether to sort the list of file names.
    drop_hidden : bool, optional, default: True
        Whether to drop hidden files from the list.
    select : str, optional
        A search string to use to select files.

    Returns
    -------
    list of str
        A list of files from the folder.
    """

    files = os.listdir(folder)

    if drop_hidden:
        files = [file for file in files if file[0] != '.']

    if drop_ext:
        files = [file.split('.')[0] for file in files]

    if sort_files:
        files.sort()

    if select:
        files = [file for file in files if select in file]

    return files


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


def make_folder(folder):
    """Make a folder.

    Parameters
    ----------
    folder : str or Path
        Folder name and location to create.
    """

    try:
        os.mkdir(folder)
    except FileExistsError:
        pass
