"""Tests for the IO functions from lisc.core."""

from py.test import raises

from lisc.core.io import *
from lisc.objs import Counts, Words
from lisc.core.errors import InconsistentDataError

from lisc.tests.utils import TestDB as TDB

###################################################################################################
###################################################################################################

def test_check_ext():

    assert check_ext('file', '.txt') == 'file.txt'
    assert check_ext('file.txt', '.txt') == 'file.txt'

def test_load_terms_file():

    tdb = TDB()
    dat = load_terms_file('test_terms', tdb)

    assert dat
    assert isinstance(dat, list)
    assert isinstance(dat[0], str)

def test_save_object():

    tdb = TDB()

    count_obj = Counts()
    words_obj = Words()

    save_object(count_obj, 'test_counts', folder=tdb)
    save_object(words_obj, 'test_words', folder=tdb)

    assert True

    with raises(InconsistentDataError):
        save_object(['bad dat'], 'test_bad', folder=tdb)

def test_load_object():

    tdb = TDB()

    counts = load_object('test_counts', folder=tdb)
    words = load_object('test_words', folder=tdb)

    assert True
