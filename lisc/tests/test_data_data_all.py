"""Tests for the DataAll() class and related functions from lisc."""

from lisc.data.data_all import *
from lisc.tests.utils import load_data
from lisc.tests.utils import TestDB as TDB

###################################################################################################
###################################################################################################

def test_data_all(tdata_full):

    # Note - constructor calls (& implicitly tests) the combine & create_freq funcs.
    dat_all = DataAll(tdata_full)

    assert dat_all

def test_check_funcs(tdata_all):

    tdata_all.check_words(2)
    tdata_all.check_kws(2)

    assert True

def test_summary(tdata_all):

    tdb = TDB()

    tdata_all.create_summary()

    assert tdata_all.summary

    tdata_all.print_summary()
    tdata_all.save_summary(folder=tdb)

    assert True
