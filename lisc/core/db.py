"""Database structure object for LISC."""

import os

###################################################################################################
###################################################################################################

PATHS = {0 : ['base'],
         1 : ['terms', 'logs', 'data', 'figs'],
         2 : ['counts', 'words', 'raw', 'summary']}

class SCDB():
    """Database object for a SCANR project.

    Attributes
    ----------
    base_path : str
        Base path for the project.
    terms_path : str
        Path to the terms folder of the project.
    logs_path : str
        Path to log files of the project.
    data_path : str
        Path to the data folder of the project.
    figs_path : str
        Path to the folder to save out figures.
    counts_path : str
        Path to the data folder for counts data.
    words_path : str
        Path to the data folder for words data.
    raw_path : str
        Path to the data folder for the raw words data.
    summary_path : str
        Path to the data folder for summaries of the words data.
    """

    def __init__(self, base_path=None, auto_gen=True):
        """Initialize SCDB object.

        Parameters
        ----------
        base_path : str
            The path to where the database is located.
        auto_gen : bool
            Whether to automatically generate all the paths for the database folders.
        """

        # Set base path for the project
        self.base_path = ("") if not base_path else base_path

        # Initialize paths
        self.terms_path = str()
        self.logs_path = str()
        self.data_path = str()
        self.figs_path = str()
        self.counts_path = str()
        self.words_path = str()
        self.raw_path = str()
        self.summary_path = str()

        # Generate project paths
        if auto_gen:
            self.gen_paths()


    def gen_paths(self):
        """Generate all the full paths for the database object."""

        self.terms_path = os.path.join(self.base_path, 'Terms')
        self.logs_path = os.path.join(self.base_path, 'Logs')
        self.data_path = os.path.join(self.base_path, 'Data')
        self.figs_path = os.path.join(self.base_path, 'Figures')

        self.counts_path = os.path.join(self.data_path, 'counts')
        self.words_path = os.path.join(self.data_path, 'words')
        self.raw_path = os.path.join(self.words_path, 'raw')
        self.summary_path = os.path.join(self.words_path, 'summary')


    def get_files(self, f_type):
        """Get a list of avaialable files in a folder in the database.

        Parameters
        ----------
        f_type : {'terms', 'logs', 'figures', 'data', 'counts', 'words', 'raw', 'summary'}
            Which folder to get the list of files from.

        Returns
        -------
        list of str
            List of files available in specified folder.
        """

        return os.listdir(getattr(self, f_type + '_path'))


    def check_file_structure(self):
        """Check the file structure of the database."""

        check_file_structure(self.base_path)

###################################################################################################
###################################################################################################

def check_folder(folder, f_type):
    """Check and extract a file path.

    Parameters
    ----------
    folder : SCDB or str or None
        A string or object containing a file path.
    f_type : {'terms', 'logs', 'figures', 'data', 'counts', 'words', 'raw', 'summary'}
        Which path to extract, if it's a SCDB object.

    Returns
    -------
    folder : str
        File path for the desired folder.

    Notes
    -----
    - If the input is an SCDB object, returns a file path as a string.
    - If the input is already a string, returns the input.
    - If the input is None, returns an empty string.
    """

    if isinstance(folder, SCDB):
        folder = getattr(folder, f_type + '_path')
    elif folder is None:
        folder = ''

    return folder


def create_file_structure(base_path=None, dir_name='lisc_db'):
    """Create the file structure for a SCANR database.

    Attributes
    ----------
    base_path : str or None
        Base path for the project.
        If none, the structure is created in th current directory.
    dir_name : str
        The name of the root folder of the directory structure.

    Returns
    -------
    db : SCDB()
        A database object for the file structure that was created.
    """

    if not base_path:
        base_path = os.getcwd()

    db = SCDB(os.path.join(base_path, dir_name))

    for level in sorted(PATHS.keys()):
        for label in PATHS[level]:
            try:
                os.mkdir(getattr(db, label + '_path'))
            except(FileExistsError):
                pass

    return db


def check_file_structure(base_path):
    """Check the file structure of a folder.

    Parameters
    ----------
    base_path : str
        Base path of the directory structure to check.
    """

    for root, _, files in os.walk(base_path):

        level = root.replace(base_path, '').count(os.sep)
        indent = ' ' * 4 * (level)

        print('{}{}/'.format(indent, os.path.basename(root)))

        subindent = ' ' * 4 * (level + 1)

        for file in files:
            if file[0] == '.':
                continue
            print('{}{}'.format(subindent, file))
