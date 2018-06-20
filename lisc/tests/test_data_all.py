"""Tests for the DataAll() class and related functions from lisc."""

from lisc.data_all import *
from lisc.tests.utils import load_data

###################################################################################
###################################################################################
###################################################################################

def test_data_all():
    """
    Note: Constructor calls (& implicitly tests) the combine & create_freq funcs.
    """

    dat = load_data(add_dat=True, n=2)

    dat_all = DataAll(dat)

    assert dat_all

def test_check_funcs():
    """   """

    dat = load_data(add_dat=True, n=2)
    dat_all = DataAll(dat)

    dat_all.check_words(2)
    dat_all.check_kws(2)

    assert True

def test_create_print_summary():
    """   """

    dat = load_data(add_dat=True, n=2)
    dat_all = DataAll(dat)

    dat_all.create_summary()

    assert dat_all.summary

    dat_all.print_summary()

    assert True
