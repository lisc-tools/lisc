"""Tests for the Base Class from lisc."""

from py.test import raises

from lisc.objects.base import Base

from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

def test_base():

    assert Base()

def test_add_terms(tbase):

    tbase.add_terms(['word', 'thing'])
    assert tbase.terms == [['word'], ['thing']]

    tbase.add_terms(['word', ['thing', 'same']])
    assert tbase.terms == [['word'], ['thing', 'same']]

    tbase.add_terms(['need', 'required'], 'inclusions')
    assert tbase.inclusions

    tbase.add_terms(['not', 'this'], 'exclusions')
    assert tbase.exclusions

def test_add_terms_file(tdb, tbase):

    tbase.add_terms_file('test_terms', directory=tdb)
    assert tbase.terms

    tbase.add_terms_file('test_inclusions', 'inclusions', directory=tdb)
    assert tbase.inclusions

    tbase.add_terms_file('test_exclusions', 'exclusions', directory=tdb)
    assert tbase.exclusions

def tests_check_terms(tbase_terms):

    tbase_terms.check_terms()
    tbase_terms.check_terms('inclusions')
    tbase_terms.check_terms('exclusions')

def test_unload_terms(tbase_terms):

    tbase_terms.unload_terms('inclusions')
    assert not tbase_terms.inclusions

    tbase_terms.unload_terms('exclusions')
    assert not tbase_terms.exclusions

    tbase_terms.unload_terms('terms')

    assert not tbase_terms.terms
    assert not tbase_terms.n_terms

def test_check_type(tbase):

    out = tbase._check_type('string')
    assert isinstance(out, list)

    out = tbase._check_type(['list'])
    assert isinstance(out, list)

def test_term_consistency(tbase_terms):

    tbase_terms._check_term_consistency()

    tbase_terms.exclusions = ['need', 'required']
    tbase_terms._check_term_consistency()

    tbase_terms.exclusions = ['not', 'avoid']
    tbase_terms._check_term_consistency()

    with raises(InconsistentDataError):
        tbase_terms.inclusions = ['need']
        tbase_terms._check_term_consistency()

    with raises(InconsistentDataError):
        tbase_terms.exclusions = ['not', 'avoid', 'bad']
        tbase_terms._check_term_consistency()
