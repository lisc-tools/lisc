"""Helper functions for testing lisc."""

import pkg_resources as pkg
from functools import wraps
from os.path import join as pjoin

from lisc.objects.base import Base
from lisc.data import Data, DataAll, Term
from lisc.core.modutils import safe_import
from lisc.core.db import SCDB, create_file_structure, check_folder

plt = safe_import('.pyplot', 'matplotlib')

###################################################################################################
###################################################################################################

class TestDB(SCDB):
    """Overloads the SCDB object as database object for test data."""

    def __init__(self):

        # Initialize from normal database object
        base = pkg.resource_filename(__name__, 'test_db')
        SCDB.__init__(self, base_path=base)

def create_files(folder):
    """Creates some test term files."""

    term_file = open(pjoin(check_folder(folder, 'terms'), 'test_terms.txt'), 'w')
    term_file.write('word\nthing, same')
    term_file.close()

    excl_file = open(pjoin(check_folder(folder, 'terms'), 'test_inclusions.txt'), 'w')
    excl_file.write('need\nrequired')
    excl_file.close()

    excl_file = open(pjoin(check_folder(folder, 'terms'), 'test_exclusions.txt'), 'w')
    excl_file.write('not\navoid')
    excl_file.close()

def load_base(set_terms=False, set_clusions=False):
    """Helper function to load Base object for testing."""

    base = Base()

    if set_terms:
        base.add_terms([['test1', 'test sin'], ['test2', 'uh oh']])

    if set_clusions:
        base.add_terms([['yeh', 'definitely'], ['need', 'required']], 'inclusions')
        base.add_terms([['exc1', 'blehh'], ['exc2', 'meh']], 'exclusions')

    return base

def load_data(add_data=False, n_data=1):
    """Helper function to load Data object for testing."""

    data = Data(Term('label', ['search'], ['inclusion'], ['exclusion']))

    if add_data:
        for ind in range(n_data):

            data.add_data('ids', 1)
            data.add_data('titles', 'title')
            data.add_data('journals', ['science', 'sc'])
            data.add_data('authors', [('A', 'B', 'C', 'D')])
            data.add_data('words', ['new', 'dat'])
            data.add_data('kws', ['lots', 'of', 'erps'])
            data.add_data('years', 2112)
            data.add_data('dois', 'doi_str')

    return data

def load_data_all():
    """Helper function to load DataAll object for testing."""

    dat = load_data(add_data=True, n_data=2)
    dat_all = DataAll(dat)

    return dat_all

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
