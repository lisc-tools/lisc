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

def test_get_item(tarts_data):

    for ind in range(tarts_data.n_articles):
        art = tarts_data[ind]
        assert art

def test_iter(tarts_data):

    for data in tarts_data:
        assert data

def test_len(tarts, tarts_data):

    assert len(tarts) == 0
    assert len(tarts_data) == len(tarts_data.ids)

def test_add_data(tarts):

    tarts.add_data('ids', 1)
    assert tarts.ids

    tarts.add_data('titles', 'title')
    assert tarts.titles

    tarts.add_data('authors', ('Last', 'First', 'IN', 'School'))
    assert tarts.authors

    tarts.add_data('journals', ('Journal name', 'J abbrev'))
    assert tarts.journals

    tarts.add_data('words', ['new', 'data'])
    assert tarts.words

    tarts.add_data('keywords', ['list', 'of', 'keywords'])
    assert tarts.keywords

    tarts.add_data('years', 2000)
    assert tarts.years

    tarts.add_data('dois', 'doi_str')
    assert tarts.dois


def test_check_results(tarts_data):

    tarts_data._check_results()

    tarts_data.ids = [1]
    with raises(InconsistentDataError):
        assert tarts_data._check_results()

def test_save(tdb, tarts_data):

    tarts_data.save(tdb)
    assert os.path.exists(os.path.join(tdb.get_folder_path('raw'), tarts_data.label + '.json'))

def test_load(tdb):

    data = Articles(Term('label', ['search'], ['inclusion'], ['exclusion']))
    data.load(tdb)

    assert data

def test_save_and_clear(tdb, tarts_data):

    tarts_data.save_and_clear(tdb)
    assert tarts_data.n_articles == 0

def test_process(tarts_data):

    tarts_data.process()
    assert tarts_data.processed

    # Check error raised if trying to process twice
    with raises(ProcessingError):
        assert tarts_data.process()
