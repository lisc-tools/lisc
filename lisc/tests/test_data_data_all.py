"""Tests for the DataAll() class and related functions from lisc."""

from lisc.data.data_all import *
from lisc.tests.utils import load_data

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

def test_create_print_summary(tdata_all):

    tdata_all.create_summary()

    assert tdata_all.summary

    tdata_all.print_summary()

    assert True
