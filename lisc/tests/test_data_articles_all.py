"""Tests for the ArticlesAll class and related functions from lisc."""

from lisc.data.articles_all import *

###################################################################################################
###################################################################################################

def test_articles_all(tarts_full):

    dat_all = ArticlesAll(tarts_full)
    assert dat_all

def test_check(tarts_all):

    tarts_all.check_frequencies(data_type='words')
    tarts_all.check_frequencies(data_type='keywords')

def test_summary(tdb, tarts_all):

    tarts_all.create_summary()

    assert tarts_all.summary

    tarts_all.print_summary()
    tarts_all.save_summary(directory=tdb)
