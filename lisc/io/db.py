"""Database structure object for LISC."""

import os
from pathlib import Path

from lisc.io.utils import get_files, make_folder

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
    The default set of paths for SCDB is:

    +-----------+---------------+------------------+-----------------------------+
    |**Level 1: Base**          |                  |                             |
    +-----------+---------------+------------------+-----------------------------+
    |terms      |Terms files.   |                  |                             |
    +-----------+---------------+------------------+-----------------------------+
    |logs       |Logs files.    |                  |                             |
    +-----------+---------------+------------------+-----------------------------+
    |figs       |Figures files. |                  |                             |
    +-----------+---------------+------------------+-----------------------------+
    |data       |Data files.    |                  |                             |
    +-----------+---------------+------------------+-----------------------------+
    |           |**Level 2: Data**                 |                             |
    +-----------+---------------+------------------+-----------------------------+
    |           |counts         |Counts data files.|                             |
    +-----------+---------------+------------------+-----------------------------+
    |           |words          |Words data files. |                             |
    +-----------+---------------+------------------+-----------------------------+
    |           |               |**Level 3: Words**|                             |
    +-----------+---------------+------------------+-----------------------------+
    |           |               |raw               |Raw words data files.        |
    +-----------+---------------+------------------+-----------------------------+
    |           |               |summary           |Summary files for words data.|
    +-----------+---------------+------------------+-----------------------------+

    """

    def __init__(self, base=None, generate_paths=True, structure=STRUCTURE):
        """Initialize a SCDB object.

        Parameters
        ----------
        base : str
            The base path to where the database is located.
        generate_paths : bool
            Whether to automatically generate all the paths for the database folders.

        Examples
        --------
        Initialize a ``SCDB`` object:

        >>> db = SCDB('lisc_db')
        """

        # Create paths dictionary, and set base path for the project
        self.paths = {}
        self.paths['base'] = Path('') if not base else Path(base)

        # Generate project paths
        if generate_paths:
            self.gen_paths(structure)


    def gen_paths(self, structure=STRUCTURE):
        """Generate all the full paths for the database object.

        Parameters
        ----------
        structure : dict, optional
            Definition of the folder structure for the database.

        Examples
        --------
        Generate paths for a ``SCDB`` object:

        >>> db = SCDB('lisc_db')
        >>> db.gen_paths()
        >>> db.paths # doctest: +NORMALIZE_WHITESPACE
        {'base': PosixPath('lisc_db'),
         'terms': PosixPath('lisc_db/terms'),
         'logs': PosixPath('lisc_db/logs'),
         'data': PosixPath('lisc_db/data'),
         'figures': PosixPath('lisc_db/figures'),
         'counts': PosixPath('lisc_db/data/counts'),
         'words': PosixPath('lisc_db/data/words'),
         'raw': PosixPath('lisc_db/data/words/raw'),
         'summary': PosixPath('lisc_db/data/words/summary')}
        """

        for level in sorted(structure):
            for upper in structure[level]:
                for label in structure[level][upper]:
                    self.paths[label] = Path(self.paths[upper]) / label


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

        Examples
        --------
        Get the path to the folder containing :class:`~.Counts` data:

        >>> db = SCDB('lisc_db')
        >>> db.get_folder_path('counts')
        PosixPath('lisc_db/data/counts')
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
            The name of the file to create the full file path for.

        Returns
        -------
        str
            The full file path to the requested file.

        Examples
        --------
        Get the path to a :class:`~.Counts` file:

        >>> db = SCDB('lisc_db')
        >>> db.get_file_path('counts', 'tutorial_counts.p')
        PosixPath('lisc_db/data/counts/tutorial_counts.p')
        """

        return self.get_folder_path(folder) / file_name


    def get_files(self, folder, drop_ext=False, sort_files=True):
        """Get a list of available files in a folder in the database.

        Parameters
        ----------
        folder : str
            Which folder path to get the list of files from.
        drop_ext : bool, optional, default: True
            Whether to drop the extensions from the list of file names.
        sort_files : bool, optional, default: True
            Whether to sort the list of files before returning.

        Returns
        -------
        files : list of str
            List of files available in specified folder.

        Examples
        --------
        Get a list of available terms files:

        >>> db = SCDB('lisc_db')
        >>> db.get_files('terms') # doctest:+SKIP
        """

        return get_files(self.get_folder_path(folder), drop_ext, sort_files)


    def check_file_structure(self):
        """Check the file structure of the database."""

        check_file_structure(self.paths['base'])

###################################################################################################
###################################################################################################

def check_directory(directory, folder=None):
    """Check and extract a file path.

    Parameters
    ----------
    directory : SCDB or str or Path or None
        A string or object containing a file path.
    folder : str, optional
        Which folder path to extract.
        Only used if `directory` is a SCDB object.

    Returns
    -------
    path : Path
        File path for the desired folder.

    Notes
    -----
    The output of this function depends on the input, as:

    - If the input is an SCDB object, returns a file path as a string.
    - If the input is already a string, returns the input.
    - If the input is None, returns an empty string.
    """

    if isinstance(directory, SCDB):
        path = directory.get_folder_path(folder)
    elif isinstance(directory, (str, Path)):
        path = directory
    elif directory is None:
        path = ''

    return Path(path)


def create_file_structure(base=None, name='lisc_db', structure=STRUCTURE):
    """Create the file structure for a SCANR database.

    Parameters
    ----------
    base : str or Path or None
        Base path for the database directory.
        If None, the structure is created in the current directory.
    name : str, optional, default: 'lisc_db'
        The name of the root folder of the directory structure.

    Returns
    -------
    db : SCDB
        A database object for the file structure that was created.

    Examples
    --------
    Create a temporary file structure for a :class:`~.SCDB` object:

    >>> import os
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as dirpath: # doctest: +SKIP
    ...     db = create_file_structure(dirpath)
    ...     for path, _, _ in os.walk(dirpath):
    ...         print(path[len(dirpath)+1:])
    <BLANKLINE>
    lisc_db
    lisc_db/figures
    lisc_db/data
    lisc_db/data/words
    lisc_db/data/words/summary
    lisc_db/data/words/raw
    lisc_db/data/counts
    lisc_db/logs
    lisc_db/terms
    """

    if not base:
        base = os.getcwd()
    base = Path(base)

    db = SCDB(base / name, structure=structure)

    # Create the base path
    make_folder(db.get_folder_path('base'))

    # Create all paths, following the database structure
    for level in sorted(structure.keys()):
        for group in structure[level].values():
            for path in group:
                make_folder(db.get_folder_path(path))

    return db


def check_file_structure(base):
    """Check the file structure of a folder.

    Parameters
    ----------
    base : str
        Base path of the directory structure to check.
    """

    for root, _, files in os.walk(base):

        level = root.replace(str(base), '').count(os.sep)
        indent = ' ' * 4 * (level)

        print('{}{}/'.format(indent, os.path.basename(root)))

        subindent = ' ' * 4 * (level + 1)

        for file in files:
            if file[0] == '.':
                continue
            print('{}{}'.format(subindent, file))


def get_structure_info(structure):
    """Get information from a directory structure definition.

    Parameters
    ----------
    structure : dict
        Definition of the directory.

    Returns
    -------
    names : list of str
        List of all the folder names (at any level).
    paths : list of str
        List of all the relative paths for all folders.
    """

    names, paths = [], []

    for level in sorted(structure):

        for label in structure[level]:

            print(level, label)

            for name in structure[level][label]:

                names.append(name)

                temp = [val for val in paths if val.split('/')[-1] == label]
                paths.append('/'.join(temp + [name]))

    return names, paths
