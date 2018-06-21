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

def test_add_id():

    dat = load_data()
    dat.add_id(1)

    assert dat.ids

def test_add_title():

    dat = load_data()
    dat.add_title('title')

    assert dat.titles

def test_add_authors():

    dat = load_data()
    dat.add_authors(('Last', 'First', 'IN', 'School'))

    assert dat.authors

def test_add_journal():

    dat = load_data()
    dat.add_journal('Journal name', 'J abbrev')

    assert dat.journals

def test_add_words():

    dat = load_data()
    dat.add_words(['new', 'dat'])

    assert dat.words

def test_add_kws():

    dat = load_data()
    dat.add_kws(['list', 'of', 'kws'])

    assert dat.kws

def test_add_pub_date():

    dat = load_data()
    dat.add_pub_date((2000, 'Feb'))

    assert dat.years
    assert dat.months

def test_add_doi():

    dat = load_data()
    dat.add_doi('doi_str')

    assert dat.dois

def test_increment_n_articles():

    dat = load_data()
    dat.increment_n_articles()

    assert dat.n_articles

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
