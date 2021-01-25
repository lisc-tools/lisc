"""Tests for lisc.utils.io."""

import os

from py.test import raises

from lisc.objects import Counts, Words

from lisc.utils.io import *

###################################################################################################
###################################################################################################

def test_check_ext():

    assert check_ext('file', '.txt') == 'file.txt'
    assert check_ext('file.txt', '.txt') == 'file.txt'

def test_load_terms_file(tdb):

    terms = load_terms_file('test_terms', tdb)

    assert terms
    assert isinstance(terms, list)
    assert isinstance(terms[0], list)
    assert isinstance(terms[0][0], str)

    # Check loading associated exclusions, should be same length
    excls1 = load_terms_file('test_exclusions', tdb)
    assert len(terms) == len(excls1)

    # Check loading file with trailing new line, should be same length
    excls2 = load_terms_file('test_exclusions_line', tdb)
    assert len(terms) == len(excls2)

def test_load_api_key(tdb):

    # Test successful load
    api_key = load_api_key('api_key', tdb)
    assert isinstance(api_key, str)

    # Test unsuccessful load, that continues
    api_key = load_api_key('bad_name', tdb)
    assert api_key is None

    # Test unsuccessful load, that fails
    with raises(FileNotFoundError):
        api_key = load_api_key('bad_name', tdb, required=True)

def test_save_object(tdb, tcounts, twords):

    save_object(tcounts, 'test_counts', directory=tdb)
    save_object(twords, 'test_words', directory=tdb)

    assert os.path.exists(os.path.join(tdb.get_folder_path('counts'), 'test_counts.p'))
    assert os.path.exists(os.path.join(tdb.get_folder_path('words'), 'test_words.p'))

    with raises(ValueError):
        save_object(['bad data'], 'test_bad', directory=tdb)

def test_load_object(tdb):

    counts = load_object('test_counts', directory=tdb)
    assert isinstance(counts, Counts)

    words = load_object('test_words', directory=tdb)
    assert isinstance(words, Words)
