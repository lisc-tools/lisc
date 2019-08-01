"""Tests for the Data class and related functions from lisc."""

import os

from py.test import raises

from lisc.data.term import Term
from lisc.tests.utils import load_data

from lisc.data.data import *

###################################################################################################
###################################################################################################

def test_data():

    assert Data(Term('label', ['search'], ['inclusion'], ['exclusion']))

def test_iter(tdata_full):

    for data in tdata_full:
        assert data

def test_add_data(tdata_empty):

    tdata_empty.add_data('ids', 1)
    assert tdata_empty.ids

    tdata_empty.add_data('titles', 'title')
    assert tdata_empty.titles

    tdata_empty.add_data('authors', ('Last', 'First', 'IN', 'School'))
    assert tdata_empty.authors

    tdata_empty.add_data('journals', ('Journal name', 'J abbrev'))
    assert tdata_empty.journals

    tdata_empty.add_data('words', ['new', 'dat'])
    assert tdata_empty.words

    tdata_empty.add_data('keywords', ['list', 'of', 'keywords'])
    assert tdata_empty.keywords

    tdata_empty.add_data('years', 2000)
    assert tdata_empty.years

    tdata_empty.add_data('dois', 'doi_str')
    assert tdata_empty.dois


def test_check_results(tdata_full):

    tdata_full._check_results()

    tdata_full.ids = [1]
    with raises(InconsistentDataError):
        assert tdata_full._check_results()

def test_save(tdb, tdata_full):

    tdata_full.save(tdb)
    assert os.path.exists(os.path.join(tdb.raw_path, tdata_full.label + '.json'))

def test_load(tdb):

    data = Data(Term('label', ['search'], ['inclusion'], ['exclusion']))
    data.load(tdb)

    assert data

def test_save_and_clear(tdb, tdata_full):

    tdata_full.save_and_clear(tdb)
    assert tdata_full.n_articles == 0
