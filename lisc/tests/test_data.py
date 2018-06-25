"""Tests for the Data() class and related functions from lisc.

Note: this should be updated to use pytest tools to use the same data object.
ToDo: add testing of saving & loading.
"""

from py.test import raises

from lisc.data import *
from lisc.tests.utils import TestDB as TDB
from lisc.tests.utils import load_data

###################################################################################################
###################################################################################################

def test_data():

    assert Data('test', ['test'])

def test_iter():

    dat = load_data(add_dat=True, n_dat=2)
    for dd in dat:
        assert dd

def test_add_id(tdata):

    tdata.add_id(1)

    assert tdata.ids

def test_add_title(tdata):

    tdata.add_title('title')

    assert tdata.titles

def test_add_authors(tdata):

    tdata.add_authors(('Last', 'First', 'IN', 'School'))

    assert tdata.authors

def test_add_journal(tdata):

    tdata.add_journal('Journal name', 'J abbrev')

    assert tdata.journals

def test_add_words(tdata):

    tdata.add_words(['new', 'dat'])

    assert tdata.words

def test_add_kws(tdata):

    tdata.add_kws(['list', 'of', 'kws'])

    assert tdata.kws

def test_add_pub_date(tdata):

    tdata.add_pub_date((2000, 'Feb'))

    assert tdata.years
    assert tdata.months

def test_add_doi(tdata):

    tdata.add_doi('doi_str')

    assert tdata.dois

def test_increment_n_articles(tdata):

    tdata.increment_n_articles()

    assert tdata.n_articles

def test_check_results():

    dat = load_data(add_dat=True)

    dat.check_results()

    dat.n_articles += 1

    with raises(InconsistentDataError):
        assert dat.check_results()

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

def test_clear():

    dat = load_data(add_dat=True)
    dat.clear()
    dat.check_results()
    assert dat.n_articles == 0

# def test_save_n_clear():

#     dat = load_data(add_dat=True)
#     dat.save_n_clear()

#     assert dat.n_articles == 0
