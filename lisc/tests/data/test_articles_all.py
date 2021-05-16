"""Tests for lisc.data.articles_all."""

from lisc.data.articles_all import *

###################################################################################################
###################################################################################################

def test_articles_all(tarts_full):

    data_all = ArticlesAll(tarts_full)
    assert data_all

def test_articles_all_none(tarts_none):

    data_all = ArticlesAll(tarts_none)
    assert data_all

def test_check(tarts_all):

    tarts_all.check_frequencies(data_type='words')
    tarts_all.check_frequencies(data_type='keywords')

def test_summary(tdb, tarts_all):

    tarts_all.create_summary()

    assert tarts_all.summary

    tarts_all.print_summary()
    tarts_all.save_summary(directory=tdb)
