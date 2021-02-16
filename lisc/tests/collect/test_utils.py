"""Tests for the lisc.collect.utils."""

from lisc.data.term import Term

from lisc.collect.utils import *

###################################################################################################
###################################################################################################

def test_make_term():

    term = Term('label', ['search1', 'search2'], ['incl1', 'incl2'], ['excl1', 'excl2'])
    arg = make_term(term)

    assert arg == "(\"search1\"OR\"search2\")AND(\"incl1\"OR\"incl2\")NOT(\"excl1\"OR\"excl2\")"

def test_make_comp():

    assert make_comp(['word']) == '("word")'
    assert make_comp(['word', 'syn1']) == '("word"OR"syn1")'
    assert make_comp(['word', 'syn1', 'syn2']) == '("word"OR"syn1"OR"syn2")'

def test_join():

    assert join('Front', 'Back', '&&') == 'Front&&Back'
    assert join('', 'Back', '&&') == 'Back'
    assert join('Front', '', '&&') == 'Front'
