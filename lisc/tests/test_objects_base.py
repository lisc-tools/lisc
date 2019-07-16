"""Tests for the Base Class from lisc."""

from py.test import raises

from lisc.objects.base import Base

from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

def test_base():

    assert Base()

def test_add_terms(tbase_empty):

    tbase_empty.add_terms(['word', 'thing'])
    assert tbase_empty.terms == [['word'], ['thing']]

    tbase_empty.add_terms(['word', ['thing', 'same']])
    assert tbase_empty.terms == [['word'], ['thing', 'same']]

def test_add_terms_file(tdb, tbase_empty):

    tbase_empty.add_terms_file('test_terms', folder=tdb)
    assert tbase_empty.terms

def tests_check_terms(tbase_terms):

    tbase_terms.check_terms()

    assert True

def test_unload_terms(tbase_terms):

    tbase_terms.unload_terms()

    assert not tbase_terms.terms
    assert not tbase_terms.n_terms

def test_get_term_labels(tbase_terms):

    tbase_terms.get_term_labels()

    assert tbase_terms.labels

def test_add_exclusions(tbase_terms):

    tbase_terms.add_exclusions(['not', 'this'])

    assert tbase_terms.exclusions

    # Check error with improper # of exclusion words
    with raises(InconsistentDataError):
        tbase_terms.add_exclusions(['bad'])

def test_add_exclusions_file(tdb, tbase_terms):

    tbase_terms.add_exclusions_file('test_exclusions', folder=tdb)
    assert tbase_terms.exclusions

def test_check_exclusions(tbase_terms_excl):

    tbase_terms_excl.check_exclusions()

    assert True

def test_unload_exclusions(tbase_terms_excl):

    tbase_terms_excl.unload_exclusions()

    assert not tbase_terms_excl.exclusions

def test_check_type(tbase_empty):

    out = tbase_empty._check_type('string')
    assert isinstance(out, list)

    out = tbase_empty._check_type(['list'])
    assert isinstance(out, list)
