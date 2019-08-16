"""Tests for the data utilities from lisc."""

from lisc.data.utils import *

###################################################################################################
###################################################################################################

def test_count_elements():

    tdat = ['a', 'b', 'a', None]
    out = count_elements(tdat)

    assert out['a'] == 2
    assert out['b'] == 1
    assert None not in out

def test_combine_lists():

    tdat = [['a', 'b'], None, ['c', 'd']]
    out = combine_lists(tdat)

    assert out == ['a', 'b', 'c', 'd']

def test_convert_string():

    string_words = 'The Last wOrd, in the bRain!'

    words_out = convert_string(string_words)
    expected = ['last', 'word', 'brain']

    assert words_out == expected

def test_lower_list():

    words = ['The',  'Cool',  'Project']

    words_out = lower_list(words)
    expected = ['the', 'cool', 'project']

    assert words_out == expected
