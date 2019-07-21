"""Tests for the BaseData class and related functions from lisc."""

from lisc.data.base_data import *

###################################################################################################
###################################################################################################

def test_base_data():
    assert BaseData('test')

def test_update_history():

    tbase_data = BaseData('test')

    tbase_data.update_history('Something happened')
    assert tbase_data.history

def test_clear():

    tbase_data = BaseData('test')

    tbase_data.ids = [1, 2, 3]

    tbase_data.clear()

    assert tbase_data.n_articles == 0
