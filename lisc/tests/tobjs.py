"""Utilties to create objects for testing."""

import pkg_resources as pkg
from itertools import repeat

from bs4.element import Tag

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

def load_tag():
    """Helper function to create a complex bs4 tag for testing."""

    tag = Tag(name='Out')
    inn1a = Tag(name='Inn1')
    inn1b = Tag(name='Inn1')

    inn1a.append('words words')
    inn1b.append('more words')

    tag.append(inn1a)
    tag.append(inn1b)

    return tag

def load_term():
    """Helper function to create a Term object for testing."""

    return Term(label='label', search=['test', 'synonym'],
                inclusions=['incl', 'incl_synonym'],
                exclusions=['excl', 'excl_synonym'])

def load_base(set_terms=False, set_clusions=False, set_labels=False, n_terms=2):
    """Helper function to load Base object for testing."""

    base = Base()

    if set_terms:
        base.add_terms(repeat_data(['test', 'synonym'], n_terms))

    if set_clusions:
        base.add_terms(repeat_data(['incl', 'incl_synonym'], n_terms), 'inclusions')
        base.add_terms(repeat_data(['excl', 'excl_synonym'], n_terms), 'exclusions')

    if set_labels:
        base.add_labels([val[0] for val in repeat_data(['label'], n_terms)])

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

def repeat_data(terms, n_times):
    """Repeat a list of data, appending index number, a specified number of times.

    Parameters
    ----------
    terms : list of str
        List of elements to repeat.
    n_times : int
        Number of times to repeat.

    Returns
    -------
    list of list of str
        List of repeated elements.
    """

    return [[val + str(ind) for val in vals] for ind, vals in enumerate(repeat(terms, n_times))]
