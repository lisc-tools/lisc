"""Tests for the scrape utilities."""

from lisc.data.term import Term

from lisc.scrape.utils import *

###################################################################################################
###################################################################################################

def test_mk_term():

    term = Term('label', ['search1', 'search2'], ['incl1', 'incl2'], ['excl1', 'excl2'])
    term_arg = mk_term(term)

    assert term_arg == "(\"search1\"OR\"search2\")AND(\"incl1\"OR\"incl2\")NOT(\"excl1\"OR\"excl2\")"

def test_mk_comp():

    assert mk_comp(['word']) == '("word")'
    assert mk_comp(['word', 'syn1']) == '("word"OR"syn1")'
    assert mk_comp(['word', 'syn1', 'syn2']) == '("word"OR"syn1"OR"syn2")'

def test_join():

    assert join('Front', 'Back', '&&') == 'Front&&Back'
    assert join('', 'Back', '&&') == 'Back'
    assert join('Front', '', '&&') == 'Front'
