"""Tests for the data utilities from lisc."""

from lisc.data.utils import *

###################################################################################################
###################################################################################################

def test_combine_lists():

    tdat = [['a', 'b'], None, ['c', 'd']]
    out = combine_lists(tdat)

    assert out == ['a', 'b', 'c', 'd']

def test_count_occurences():

    tdat = ['a', 'b', 'a']
    out = count_occurences(tdat)

    assert out == [(2, 'a'), (1, 'b')]
