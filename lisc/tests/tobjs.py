"""Utilties to create objects for testing."""

import pkg_resources as pkg

from lisc.objects.base import Base
from lisc.data import Articles, ArticlesAll, Term

from lisc.utils.db import SCDB

###################################################################################################
###################################################################################################

class TestDB(SCDB):
    """Overloads the SCDB object as database object for tests."""

    def __init__(self):

        # Initialize from normal database object
        base = pkg.resource_filename(__name__, 'test_db')
        SCDB.__init__(self, base=base)

def load_base(set_terms=False, set_clusions=False):
    """Helper function to load Base object for testing."""

    base = Base()

    if set_terms:
        base.add_terms([['test1', 'test sin'], ['test2', 'uh oh']])

    if set_clusions:
        base.add_terms([['yeh', 'definitely'], ['need', 'required']], 'inclusions')
        base.add_terms([['exc1', 'blehh'], ['exc2', 'meh']], 'exclusions')

    return base

def load_arts(add_data=False, n_data=1):
    """Helper function to load Articles object for testing."""

    arts = Articles(Term('label', ['search'], ['inclusion'], ['exclusion']))

    if add_data:
        for ind in range(n_data):

            arts.add_data('ids', 1)
            arts.add_data('titles', 'title')
            arts.add_data('journals', ['science', 'sc'])
            arts.add_data('authors', [('A', 'B', 'C', 'D')])
            arts.add_data('words', 'Lots of words data.')
            arts.add_data('keywords', ['lots', 'of', 'keywords'])
            arts.add_data('years', 2112)
            arts.add_data('dois', 'doi_str')

    return arts

def load_arts_all():
    """Helper function to load ArticlesAll object for testing."""

    arts = load_arts(add_data=True, n_data=2)
    arts_all = ArticlesAll(arts)

    return arts_all
