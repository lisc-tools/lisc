"""Tests for the IO functions from lisc.core."""

import os

from py.test import raises

from lisc.objects import Counts, Words

from lisc.core.io import *

###################################################################################################
###################################################################################################

def test_check_ext():

    assert check_ext('file', '.txt') == 'file.txt'
    assert check_ext('file.txt', '.txt') == 'file.txt'

def test_load_terms_file(tdb):

    terms = load_terms_file('test_terms', tdb)

    assert terms
    assert isinstance(terms, list)
    assert isinstance(terms[0], str)

def test_save_object(tdb, tcounts, twords):

    save_object(tcounts, 'test_counts', folder=tdb)
    save_object(twords, 'test_words', folder=tdb)

    assert os.path.exists(os.path.join(tdb.counts_path, 'test_counts.p'))
    assert os.path.exists(os.path.join(tdb.words_path, 'test_words.p'))

    with raises(ValueError):
        save_object(['bad dat'], 'test_bad', folder=tdb)

def test_load_object(tdb):

    counts = load_object('test_counts', folder=tdb)
    assert isinstance(counts, Counts)

    words = load_object('test_words', folder=tdb)
    assert isinstance(words, Words)
