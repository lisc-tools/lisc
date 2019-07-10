"""Tests for the Data class and related functions from lisc."""

from py.test import raises

from lisc.data.data import *
from lisc.tests.utils import TestDB as TDB
from lisc.tests.utils import load_data

###################################################################################################
###################################################################################################

def test_data():

    assert Data('test', ['test'])

def test_iter(tdata_full):

    for dat in tdata_full:
        assert dat

def test_add_id(tdata_empty):

    tdata_empty.add_id(1)

    assert tdata_empty.ids

def test_add_title(tdata_empty):

    tdata_empty.add_title('title')

    assert tdata_empty.titles

def test_add_authors(tdata_empty):

    tdata_empty.add_authors(('Last', 'First', 'IN', 'School'))

    assert tdata_empty.authors

def test_add_journal(tdata_empty):

    tdata_empty.add_journal('Journal name', 'J abbrev')

    assert tdata_empty.journals

def test_add_words(tdata_empty):

    tdata_empty.add_words(['new', 'dat'])

    assert tdata_empty.words

def test_add_kws(tdata_empty):

    tdata_empty.add_kws(['list', 'of', 'kws'])

    assert tdata_empty.kws

def test_add_pub_date(tdata_empty):

    tdata_empty.add_pub_date((2000, 'Feb'))

    assert tdata_empty.years
    assert tdata_empty.months

def test_add_doi(tdata_empty):

    tdata_empty.add_doi('doi_str')

    assert tdata_empty.dois

def test_increment_n_articles(tdata_empty):

    tdata_empty.increment_n_articles()

    assert tdata_empty.n_articles

def test_check_results(tdata_full):

    tdata_full.check_results()

    tdata_full.n_articles += 1

    with raises(InconsistentDataError):
        assert tdata_full.check_results()

def test_update_history():

    pass

# def test_save():

#     tdb = TDB()

#     dat = load_data(add_dat=True)

#     dat.save(tdb)

#     assert True

# def test_load():

#     tdb = TDB()

#     dat = Data('test')
#     dat.load(tdb)

#     assert dat

def test_clear(tdata_full):

    tdata_full.clear()
    tdata_full.check_results()
    assert tdata_full.n_articles == 0

# def test_save_n_clear():

#     dat = load_data(add_dat=True)
#     dat.save_n_clear()

#     assert dat.n_articles == 0
