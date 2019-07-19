"""Tests for the Data class and related functions from lisc."""

import os

from py.test import raises

from lisc.data.data import *
from lisc.tests.utils import load_data

###################################################################################################
###################################################################################################

def test_data():

    assert Data('test')

def test_iter(tdata_full):

    for dat in tdata_full:
        assert dat

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

    tdata_empty.add_data('kws', ['list', 'of', 'kws'])
    assert tdata_empty.kws

    tdata_empty.add_data('years', 2000)
    assert tdata_empty.years

    tdata_empty.add_data('dois', 'doi_str')
    assert tdata_empty.dois


def test_check_results(tdata_full):

    tdata_full.check_results()

    tdata_full.ids = [1]

    with raises(InconsistentDataError):
        assert tdata_full.check_results()

def test_save(tdb, tdata_full):

    tdata_full.save(tdb)
    assert os.path.exists(os.path.join(tdb.raw_path, 'test.json'))

def test_load(tdb):

    data = Data('test')
    data.load(tdb)

    assert data

def test_save_n_clear(tdb, tdata_full):

    tdata_full.save_n_clear(tdb)
    assert tdata_full.n_articles == 0
