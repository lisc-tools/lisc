"""Tests for the BaseData class and related functions from lisc."""

from lisc.data.base_data import *

###################################################################################################
###################################################################################################

def test_base_data():

    assert BaseData('test')

def test_clear():

    tbase_data = BaseData('test')
    tbase_data.ids = [1, 2, 3]
    tbase_data.clear()

    assert tbase_data.n_articles == 0
