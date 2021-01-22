"""Tests for lisc.data.base_articles."""

from lisc.data.base_articles import *

###################################################################################################
###################################################################################################

def test_base_articles():

    assert BaseArticles('test')

def test_clear():

    tbase_arts = BaseArticles('test')
    tbase_arts.ids = [1, 2, 3]
    tbase_arts.clear()

    assert tbase_arts.n_articles == 0
