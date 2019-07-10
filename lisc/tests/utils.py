"""Helper functions for testing lisc."""

import pkg_resources as pkg
from functools import wraps

from lisc.objs.base import Base
from lisc.data import Data, DataAll
from lisc.core.db import SCDB
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')

###################################################################################################
###################################################################################################

class TestDB(SCDB):
    """Overloads the SCDB object as database object for test data."""

    def __init__(self):

        # Initialize from normal database object
        SCDB.__init__(self, auto_gen=False)

        # Set up the base path to tests data
        self.base_path = pkg.resource_filename(__name__, 'test_db')
        self.gen_paths()

###################################################################################################
###################################################################################################

def load_base(set_terms=False, set_excl=False):
    """Helper function to load Base object for testing."""

    base = Base()

    if set_terms:
        base.set_terms([['test1', 'test sin'], ['test2', 'uh oh']])

    if set_excl:
        base.set_exclusions([['exc1', 'blehh'], ['exc2', 'meh']])

    return base

def load_data(add_dat=False, n_dat=1):
    """Helper function to load Data object for testing."""

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

def load_data_all():
    """Helper function to load DataAll object for testing."""

    dat = load_data(add_dat=True, n_dat=2)
    dat_all = DataAll(dat)

    return dat_all

###################################################################################################
###################################################################################################

def plot_test(func):
    """Decorator for simple testing of plotting functions.

    Notes
    -----
    This decorator closes all plots prior to the test.
    After running the test function, it checks an axis was created with data.
    It therefore performs a minimal test - asserting the plots exists, with no accuracy checking.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        plt.close('all')

        func(*args, **kwargs)

        ax = plt.gca()
        assert ax.has_data()

    return wrapper


def optional_test(dependency):
    """Decorator to only run a test if the specified optional dependency is present.

    Parameters
    ----------
    dependency : str
        The name of an optional dependency to test import of.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if safe_import(dependency):
                return func(*args, **kwargs)

        return wrapper

    return decorator
