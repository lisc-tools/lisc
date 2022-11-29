"""Tests for lisc.data.articles."""

import os

from pytest import raises

from lisc.data.term import Term

from lisc.data.articles import *

###################################################################################################
###################################################################################################

def test_articles():

    arts = Articles(Term('label', ['search'], ['inclusion'], ['exclusion']))
    assert isinstance(arts, Articles)

def test_get_item(tarts_full):

    for ind in range(tarts_full.n_articles):
        art = tarts_full[ind]
        assert art

def test_iter(tarts_full):

    for data in tarts_full:
        assert data

def test_len(tarts_empty, tarts_full):

    assert len(tarts_empty) == 0
    assert len(tarts_full) == len(tarts_full.ids)

def test_add_data(tarts_empty):

    tarts_empty.add_data('ids', 1)
    assert tarts_empty.ids

    tarts_empty.add_data('titles', 'title')
    assert tarts_empty.titles

    tarts_empty.add_data('authors', ('Last', 'First', 'IN', 'School'))
    assert tarts_empty.authors

    tarts_empty.add_data('journals', ('Journal name', 'J abbrev'))
    assert tarts_empty.journals

    tarts_empty.add_data('words', ['new', 'data'])
    assert tarts_empty.words

    tarts_empty.add_data('keywords', ['list', 'of', 'keywords'])
    assert tarts_empty.keywords

    tarts_empty.add_data('years', 2000)
    assert tarts_empty.years

    tarts_empty.add_data('dois', 'doi_str')
    assert tarts_empty.dois


def test_check_results(tarts_full):

    tarts_full._check_results()

    tarts_full.ids = [1]
    with raises(InconsistentDataError):
        assert tarts_full._check_results()

def test_save(tdb, tarts_full):

    tarts_full.save(tdb)
    assert os.path.exists(os.path.join(tdb.get_folder_path('raw'), tarts_full.label + '.json'))

def test_load(tdb):

    data = Articles(Term('label', ['search'], ['inclusion'], ['exclusion']))
    data.load(tdb)

    assert data

def test_save_and_clear(tdb, tarts_full):

    tarts_full.save_and_clear(tdb)
    assert tarts_full.n_articles == 0

def test_process(tarts_full):

    tarts_full.process()
    assert tarts_full.processed
