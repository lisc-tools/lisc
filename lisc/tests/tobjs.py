"""Utilties to create objects for testing."""

from copy import deepcopy
from itertools import repeat

from bs4.element import Tag

import numpy as np

from lisc.objects.base import Base
from lisc.objects import Counts1D, Counts, Words
from lisc.data import Articles, ArticlesAll, Term

from lisc.io.db import SCDB

from lisc.tests.tsettings import TEST_DB_PATH

###################################################################################################
###################################################################################################

class TestDB(SCDB):
    """Overloads the SCDB object as database object for tests."""

    def __init__(self):

        # Initialize from normal database object
        SCDB.__init__(self, base=TEST_DB_PATH)

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

def load_meta_dict():
    """Helper function to create a dictionary of meta data information."""

    return {
        'date': '1999-12-31_00:00:00',
        'log': None,
        'requester_n_requests': 1,
        'requester_wait_time': 1,
        'requester_start_time': '00:00:00 Friday 01 January 2000',
        'requester_end_time': '00:00:00 Monday 01 January 2000',
        'requester_logging': None,
        'db_info_dbname': 'pubmed',
        'db_info_menuname': 'PubMed',
        'db_info_description': 'PubMed bibliographic record',
        'db_info_dbbuild': 'Build-#####',
        'db_info_count': '123456789',
        'db_info_lastupdate': '1999/12/31 00:00',
        'settings_setting1' : True,
        'settings_setting2' : 42,
    }

def load_base(add_terms=False, add_clusions=False, add_labels=False, n_terms=2):
    """Helper function to load Base object for testing."""

    base = Base()

    if add_terms:
        base.add_terms(repeat_data(['test', 'synonym'], n_terms))

    if add_clusions:
        base.add_terms(repeat_data(['incl', 'incl_synonym'], n_terms), 'inclusions')
        base.add_terms(repeat_data(['excl', 'excl_synonym'], n_terms), 'exclusions')

    if add_labels:
        base.add_labels([val[0] for val in repeat_data(['label'], n_terms)])

    return base

def load_counts1d(add_terms=False, add_data=False, n_terms=2):
    """Helper function to load Counts1D object for testing."""

    counts1d = Counts1D()

    if add_terms:
        counts1d.add_terms(repeat_data(['test', 'synonym'], n_terms))

    if add_data:
        counts1d.counts = np.random.randint(0, 100, (2))

    return counts1d

def load_counts(add_terms=False, add_data=False, n_terms=(2, 2)):
    """Helper function to load Counts object for testing."""

    counts = Counts()

    if add_terms:
        counts1d.add_terms(repeat_data(['test', 'synonym'], n_terms[0]), dim='A')
        counts1d.add_terms(repeat_data(['test', 'synonym'], n_terms[1]), dim='B')

    if add_data:
        counts.terms['A'].counts = np.random.randint(0, 100, (n_terms[0]))
        counts.terms['B'].counts = np.random.randint(0, 100, (n_terms[1]))
        counts.counts = np.random.randint(0, 100, n_terms)

    return counts

def load_words(add_terms=False, add_data=False, n_terms=2):
    """Helper function to load Words object for testing."""

    words = Words()

    if add_terms:
        words.add_terms(repeat_data(['test', 'synonym'], n_terms))

    if add_data:
        arts = load_arts(add_data=True, n_data=2)
        words.results = [deepcopy(arts) for ind in range(n_terms)]

    return words

def load_arts(add_data=False, n_data=1, add_none=False):
    """Helper function to load Articles object for testing."""

    arts = Articles(Term('label', ['search'], ['inclusion'], ['exclusion']))

    if add_data:
        for ind in range(n_data):

            arts.add_data('ids', ind)
            arts.add_data('titles', 'title')
            arts.add_data('journals', ['science', 'sc'])
            arts.add_data('authors', [['ln1', 'fn1', 'in1', 'af1'], ['ln2', 'fn2', 'in2', 'af2']])
            arts.add_data('words', 'Lots of words data. Just a continuous text.')
            arts.add_data('keywords', ['lots', 'of', 'keywords'])
            arts.add_data('years', 2112)
            arts.add_data('dois', 'doi_str')

    if add_none:
        arts.dois[-1] = None
        arts.years[-1] = None
        arts.authors[-1] = None
        arts.words[-1] = str()
        arts.keywords[-1] = list()

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
