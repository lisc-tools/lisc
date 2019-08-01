"""Tests for the DataAll() class and related functions from lisc."""

from lisc.data.data_all import *
from lisc.tests.utils import load_data

###################################################################################################
###################################################################################################

def test_data_all(tdata_full):

    dat_all = DataAll(tdata_full)
    assert dat_all

def test_check(tdata_all):

    tdata_all.check_frequencies(data='words')
    tdata_all.check_frequencies(data='keywords')

def test_summary(tdb, tdata_all):

    tdata_all.create_summary()

    assert tdata_all.summary

    tdata_all.print_summary()
    tdata_all.save_summary(folder=tdb)
