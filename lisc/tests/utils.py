"""Helper functions for testing lisc."""

import pkg_resources as pkg

from lisc.base import Base
from lisc.data import Data
from lisc.core.db import SCDB

###################################################################################################
###################################################################################################

class TestDB(SCDB):
    """Overloads the SCDB object as database object for test data."""

    def __init__(self):

        # Initialize from OMDB object
        SCDB.__init__(self, auto_gen=False)

        # Set up the base path to tests data
        self.project_path = pkg.resource_filename(__name__, 'data')
        self.gen_paths()

###################################################################################################
###################################################################################################

def load_base(set_terms=False, set_excl=False):
    """Helper function to load Base() object for testing."""

    base = Base()

    if set_terms:
        base.set_terms_file('test')

    if set_excl:
        base.set_exclusions_file('test_excl')

    return base

def load_data(add_dat=False, n_dat=1):
    """Helper function to load Data() object for testing."""

    dat = Data('test', ['test'])

    if add_dat:
        for i in range(n_dat):
            dat.add_id(1)
            dat.add_title('title')
            dat.add_journal('science', 'sc')
            dat.add_authors([('A', 'B', 'C', 'D')])
            dat.add_words(['new', 'dat'])
            dat.add_kws(['lots', 'of', 'erps'])
            dat.add_pub_date((2112, 'Jan'))
            dat.add_doi('doi_str')
            dat.increment_n_articles()

    return dat
