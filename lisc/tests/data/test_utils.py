"""Tests for lisc.data.utils."""

from string import punctuation
from collections import Counter

from lisc.data.utils import *

###################################################################################################
###################################################################################################

def test_count_elements():

    tdata = ['a', 'b', 'a', None]
    out = count_elements(tdata)

    assert out['a'] == 2
    assert out['b'] == 1
    assert None not in out

def test_threshold_counter():

    tcounter = Counter({'A' : 2, 'B' : 4})
    out = threshold_counter(tcounter, 3)
    assert len(out) == 1
    assert out['B'] == tcounter['B']
    assert 'A' not in out

def test_drop_none():

    tdata = ['A', 'B', 'C', None, 'D', None, 'E']
    for el in drop_none(tdata):
        assert el in tdata
        assert el is not None

def test_combine_lists():

    tdata = [['a', 'b'], None, ['c', 'd']]
    out = combine_lists(tdata)

    assert out == ['a', 'b', 'c', 'd']

def test_tokenize():

    tdata = "This is a sentence full of stuff. Like, words! And ideas: and things."

    tokens = tokenize(tdata)
    assert isinstance(tokens, list)
    assert tokens[0] == 'This'
    assert tokens[-1] == 'things'
    assert len(tokens) == 13

def test_convert_string():

    string_words = 'The Last wOrd, in the bRain!'

    words_out = convert_string(string_words)
    expected = ['last', 'word', 'brain']

    assert words_out == expected

def test_lower_list():

    words = ['The', 'Cool', 'Project']

    words_out = lower_list(words)
    expected = ['the', 'cool', 'project']

    assert words_out == expected
