"""Tests for the Base Class from lisc.

NOTES
-----
- Load from file method '_file' are only tested for default (from module) loads.
"""

from py.test import raises

from lisc.base import Base, _check_type, _terms_load_file

from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

def test_check_type():

    out = _check_type('string')
    assert isinstance(out, list)

    out = _check_type(['list'])
    assert isinstance(out, list)

def test_terms_load_file():

    dat = _terms_load_file('test')

    assert dat
    assert isinstance(dat, list)
    assert isinstance(dat[0], str)

####################################################################################################
####################################################################################################

def test_base():

    assert Base()

def test_set_terms(tbase_empty):

    tbase_empty.set_terms(['word', 'thing'])

    assert tbase_empty.terms

def test_set_terms_file(tbase_empty):

    tbase_empty.set_terms_file('test')

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

def test_set_exclusions(tbase_terms):

    tbase_terms.set_exclusions(['not', 'this'])

    assert tbase_terms.exclusions

def test_set_exclusions_error(tbase_terms):

    # Check error with improper # of exclusion words
    with raises(InconsistentDataError):
        tbase_terms.set_exclusions(['bad'])

def test_set_exclusions_file(tbase_terms):

    tbase_terms.set_exclusions_file('test_excl')

    assert tbase_terms.exclusions

def test_check_exclusions(tbase_terms_excl):

    tbase_terms_excl.check_exclusions()

    assert True

def test_unload_exclusions(tbase_terms_excl):

    tbase_terms_excl.unload_exclusions()

    assert not tbase_terms_excl.exclusions
