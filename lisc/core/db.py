"""Database structure object for the LISC project."""

import os

###################################################################################################
###################################################################################################

class SCDB(object):
    """Class to hold database information for SCANR project.

    Attributes
    ----------
    project_path : str
        Base path to the ERPSC project.
    data_path : str
        Path to the data folder of the ERPSC project.
    counts_path : str
        Path to the data folder for counts data.
    words_path : str
        Path to the data folder for words data.
    figs_path : str
        Path to the folder to save out figures.
    """

    def __init__(self, project_path=None, auto_gen=True):
        """Initialize SCDB object."""

        # Set base path for the project
        if not project_path:
            self.project_path = ("")
        else:
            self.project_path = project_path

        # Initialize paths
        self.data_path = str()
        self.counts_path = str()
        self.words_path = str()
        self.figs_path = str()

        # Generate project paths
        if auto_gen:
            self.gen_paths()


    def gen_paths(self):
        """Generate all the full paths for the ERP-SCANR project."""

        # Set the data path
        self.data_path = os.path.join(self.project_path, 'Data')
        self.figs_path = os.path.join(self.project_path, 'Figures')

        # Set paths to different data types
        self.counts_path = os.path.join(self.data_path, 'counts')
        self.words_path = os.path.join(self.data_path, 'words')


class WebDB(object):
    """Class to hold database information for SCANR Website.

    Parameters
    ----------
    base_path : str
        Path to base directory of website.
    post_path : str
        Path to posts directory.
    dat_path : str
        Path to data directory.
    plt_path : str
        Path to store plots.
    """

    def __init__(self):
        """Initialize WebDB object."""

        # Set base path for the website
        self.base_path = ("")

        # Set paths to directories for the website
        self.post_path = os.path.join(self.base_path, '_posts')
        self.dat_path = os.path.join(self.base_path, '_data')
        self.plt_path = os.path.join(self.base_path, 'assets/TERMs')

###################################################################################################
###################################################################################################

def check_db(db):
    """Check if SCDB object is initialized, if not, return an SCDB object.

    Parameters
    ----------
    db : SCDB() object, or None
        Database object for LISC project.

    Returns
    -------
    db : SCDB() object
        Database object for LISC project.
    """

    # If db is currently None, initialize as SCDB
    return SCDB() if not db else db
