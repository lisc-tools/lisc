"""Tests for lisc.io.io"""

import os

from pytest import raises

from lisc.data import MetaData
from lisc.objects import Counts, Words

from lisc.io.io import *

###################################################################################################
###################################################################################################

def test_load_txt_file(tdb):

    terms = load_txt_file('test_terms', tdb)

    assert terms
    assert isinstance(terms, list)
    assert isinstance(terms[0], list)
    assert isinstance(terms[0][0], str)

    # Check loading associated exclusions, should be same length
    excls1 = load_txt_file('test_exclusions', tdb)
    assert len(terms) == len(excls1)

    # Check loading file with trailing new line, should be same length
    excls2 = load_txt_file('test_exclusions_line', tdb)
    assert len(terms) == len(excls2)

    # Check loading a file without splitting elements within each line
    labels = load_txt_file('test_labels', tdb, split_elements=False)
    assert labels
    assert isinstance(labels, list)
    assert isinstance(labels[0], str)

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

def test_save_meta_data(tdb, tmetadata):

    save_meta_data(tmetadata, 'test_meta_save', tdb)
    assert os.path.exists(os.path.join(tdb.get_folder_path('logs'), 'test_meta_save.json'))

def test_load_meta_data(tdb):

    meta_data = load_meta_data('test_meta_save', tdb)
    assert isinstance(meta_data, MetaData)
