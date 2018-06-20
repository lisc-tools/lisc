"""Helper functions for testing lisc."""

import pkg_resources as pkg

from lisc.base import Base
from lisc.data import Data
from lisc.core.db import SCDB

##################################################################################
##################################################################################
##################################################################################

class TestDB(SCDB):
    """Overloads the SCDB object as database object for test data."""

    def __init__(self):

        # Initialize from OMDB object
        SCDB.__init__(self, auto_gen=False)

        # Set up the base path to tests data
        self.project_path = pkg.resource_filename(__name__, 'data')
        self.gen_paths()

##################################################################################
##################################################################################
##################################################################################

def load_base(set_erps=False, set_excl=False, set_terms=None):
    """Helper function to load Base() object for testing."""

    base = Base()

    if set_erps:
        base.set_erps_file()

    if set_excl:
        base.set_exclusions_file()

    if set_terms:
        base.set_terms_file(set_terms)

    return base

def load_data(add_dat=False, n=1):
    """Helper function to load Data() object for testing."""

    dat = Data('test', ['test'])

    if add_dat:
        for i in range(n):
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
