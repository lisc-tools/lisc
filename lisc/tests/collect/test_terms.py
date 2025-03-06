"""Tests for the lisc.collect.terms."""

from pytest import raises

from lisc.data.term import Term

from lisc.collect.terms import *

###################################################################################################
###################################################################################################

def test_check_joiner():

    for joiner in JOINERS:
        check_joiner(joiner)
    with raises(ValueError):
        check_joiner('ANDD')

def test_make_term():

    term1 = Term('label', ['search'], ['incl'], ['excl'])
    out1 = make_term(term1)
    assert out1 == '("search")AND("incl")NOT("excl")'

    term2 = Term('label', ['search1', 'search2'], ['incl1', 'incl2'], ['excl1', 'excl2'])
    out2 = make_term(term2)
    assert out2 == '("search1"OR"search2")AND("incl1"OR"incl2")NOT("excl1"OR"excl2")'

def test_make_comp():

    assert make_comp(['word'], 'OR') == '("word")'
    assert make_comp(['word', 'syn1'], 'OR') == '("word"OR"syn1")'
    assert make_comp(['word', 'syn1'], 'AND') == '("word"AND"syn1")'
    assert make_comp(['word', 'syn1', 'syn2'], 'OR') == '("word"OR"syn1"OR"syn2")'
    assert make_comp(['word', 'syn1', 'syn2'], 'AND') == '("word"AND"syn1"AND"syn2")'
    assert make_comp(['compound word'], 'OR') == '("compound+word")'

def test_join():

    join1 = join('("term1")', '("incl1")', joiner='AND')
    assert join1 == '("term1")AND("incl1")'

    join2 = join('("term1a"OR"term1b")', '("incl1a"OR"incl1b")', joiner='AND')
    assert join2 == '("term1a"OR"term1b")AND("incl1a"OR"incl1b")'

    join3 = join('("term1a"OR"term1b")', '("incl1a"OR"incl1b")', joiner='OR')
    join3 == '("term1a"OR"term1b")OR("incl1a"OR"incl1b")'

    join4 = join('("term1")', '', joiner='OR')
    assert join4 == '("term1")'

    join5 = join('', '("term1")', joiner='OR')
    assert join5 == '("term1")'

def test_join_multi():

    joined1 = join_multi(['("term1")', '("incl1")', '("excl1")'], ['AND', 'NOT'])
    assert joined1 == '("term1")AND("incl1")NOT("excl1")'

    joined2 = join_multi(\
        ['("term2"OR"term2b")', '("incl2"OR"incl2b")', '("excl2"OR"excl2b")'], ['AND', 'NOT'])
    assert joined2 == '("term2"OR"term2b")AND("incl2"OR"incl2b")NOT("excl2"OR"excl2b")'
