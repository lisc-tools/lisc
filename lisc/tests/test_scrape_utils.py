"""Tests for the scrape utilities."""

from lisc.scrape.utils import *

###################################################################################################
###################################################################################################

def test_comb_terms():

    out = comb_terms(['one', 'two'], 'or')
    assert out == '("one"OR"two")'

    out = comb_terms(['one', 'two'], 'not')
    assert out == 'NOT"one"NOT"two"'

def test_mk_term():
    pass
