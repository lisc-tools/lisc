"""Database structure object for LISC."""

import os

###################################################################################################
###################################################################################################

STRUCTURE = {1 : {'base' : ['terms', 'logs', 'data', 'figures']},
             2 : {'data' : ['counts', 'words']},
             3 : {'words' : ['raw', 'summary']}}

class SCDB():
    """Database object for a SCANR project.

    Attributes
    ----------
    paths : dict
        Dictionary of all folder paths in the project.

    Notes
    -----
    The default set of paths for a SCDB object is:
    - terms                 Term files.
    - logs                  Log files.
    - figs                  Figure files.
    - data                  Data files.
        - counts            Counts data files.
        - words             Words data files.
            - raw           Raw words data files
            - summary       Summary files for words data.
    """

    def __init__(self, base=None, generate_paths=True, structure=STRUCTURE):
        """Initialize SCDB object.

        Parameters
        ----------
        base : str
            The base path to where the database is located.
        generate_paths : bool
            Whether to automatically generate all the paths for the database folders.
        """

        # Create paths dictionary, and set base path for the project
        self.paths = {}
        self.paths['base'] = ("") if not base else base

        # Generate project paths
        if generate_paths:
            self.gen_paths(structure)


    def gen_paths(self, structure=STRUCTURE):
        """Generate all the full paths for the database object.

        Parameters
        ----------
        structure : dict, optional
            Definition of the folder structure for the database.
        """

        for level in structure:
            for upper in structure[level]:
                for label in structure[level][upper]:
                    self.paths[label] = os.path.join(self.paths[upper], label)


    def get_folder_path(self, folder):
        """Get the path to a folder in the directory.

        Parameters
        ----------
        folder : str
            Which folder to get the path for.

        Returns
        -------
        str
            The path to the requested directory folder.
        """

        if folder not in self.paths.keys():
            raise ValueError('Requested folder not available in directory structure.')

        return self.paths[folder]


    def get_file_path(self, folder, file_name):
        """Get a path to a file in a designated directory folder.

        Parameters
        ----------
        folder : str
            Which folder path to get the file path from.
        file_name : str
            The name of the file to create the fulle path for

        Returns
        -------
        str
            The full file path to the requested file.
        """

        return os.path.join(self.get_folder_path(folder), file_name)


    def get_files(self, folder):
        """Get a list of available files in a folder in the database.

        Parameters
        ----------
        folder : str
            Which folder path to get the list of files from.

        Returns
        -------
        list of str
            List of files available in specified folder.
        """

        return os.listdir(self.get_folder_path(folder))


    def check_file_structure(self):
        """Check the file structure of the database."""

        check_file_structure(self.paths['base'])

###################################################################################################
###################################################################################################

def check_directory(directory, folder):
    """Check and extract a file path.

    Parameters
    ----------
    directory : SCDB or str or None
        A string or object containing a file path.
    folder : str
        Which folder path to extract, if it's a SCDB object.

    Returns
    -------
    path : str
        File path for the desired folder.

    Notes
    -----
    - If the input is an SCDB object, returns a file path as a string.
    - If the input is already a string, returns the input.
    - If the input is None, returns an empty string.
    """

    if isinstance(directory, SCDB):
        path = directory.get_folder_path(folder)
    elif isinstance(directory, str):
        path = directory
    elif directory is None:
        path = ''

    return path


def create_file_structure(base=None, name='lisc_db', structure=STRUCTURE):
    """Create the file structure for a SCANR database.

    Attributes
    ----------
    base : str or None
        Base path for the database directory.
        If None, the structure is created in the current directory.
    name : str
        The name of the root folder of the directory structure.

    Returns
    -------
    db : SCDB()
        A database object for the file structure that was created.
    """

    if not base:
        base = os.getcwd()

    db = SCDB(os.path.join(base, name), structure=structure)

    # Create the base path
    os.mkdir(db.get_folder_path('base'))

    # Create all paths, following the database structure
    for level in sorted(structure.keys()):
        for group in structure[level].values():
            for path in group:
                try:
                    os.mkdir(db.get_folder_path(path))
                except(FileExistsError):
                    pass

    return db


def check_file_structure(base):
    """Check the file structure of a folder.

    Parameters
    ----------
    base : str
        Base path of the directory structure to check.
    """

    for root, _, files in os.walk(base):

        level = root.replace(base, '').count(os.sep)
        indent = ' ' * 4 * (level)

        print('{}{}/'.format(indent, os.path.basename(root)))

        subindent = ' ' * 4 * (level + 1)

        for file in files:
            if file[0] == '.':
                continue
            print('{}{}'.format(subindent, file))
