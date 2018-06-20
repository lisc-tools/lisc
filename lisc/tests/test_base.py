"""Tests for the Base Class from lisc.

NOTES
-----
- Load from file method '_file' are only tested for default (from module) loads.
"""

from py.test import raises

from lisc.base import Base, _check_type, _terms_load_file

from lisc.tests.utils import load_base
from lisc.core.errors import InconsistentDataError

###################################################################################################
############################ TESTS - LISC - BASE - PRIVATE FUNCTIONS  ############################
###################################################################################################

def test_check_type():
    """Test that the _check_type function works properly."""

    out = _check_type('string')
    assert isinstance(out, list)

    out = _check_type(['list'])
    assert isinstance(out, list)

# def test_terms_load_file():
#     """Test that the _terms_load_file function returns properly."""

#     dat = _terms_load_file('test')
#     cog_terms_dat = _terms_load_file('test')
#     dis_terms_dat = _terms_load_file('test')
#     excl_dat = _terms_load_file('test')

#     all_dat = [dat, cog_terms_dat, dis_terms_dat, excl_dat]

#     for dat in all_dat:
#         assert dat
#         assert isinstance(dat, list)
#         assert isinstance(dat[0], str)

####################################################################################################
################################## TESTS - LISC - GENERAL - BASE ##################################
####################################################################################################

def test_base():

    assert Base()

def test_set_terms():

    base = load_base()
    base.set_terms(['word', 'thing'])

    assert base.terms

def test_set_terms_file():

    base = load_base()
    base.set_terms_file('test')

    assert base.terms

def tests_check_terms():

    base = load_base(set_terms=True)

    base.check_terms()

    assert True

def test_unload_terms():

    base = load_base(set_terms=True)

    base.unload_terms()

    assert not base.terms
    assert not base.n_terms

def test_set_exclusions():

    base = Base()
    base.set_terms(['word', 'thing'])
    base.set_exclusions(['not', 'this'])

    assert base.exclusions

    # Check error with improper # of exclusion words
    base = Base()
    base.set_terms(['word', 'thing'])

    with raises(InconsistentDataError):
        base.set_exclusions(['bad'])

def test_set_exclusions_file():

    base = load_base(set_terms=True)
    base.set_exclusions_file('test_excl')

    assert base.exclusions

def test_check_exclusions():

    base = load_base(set_terms=True, set_excl=True)

    base.check_exclusions()

    assert True

def test_unload_exclusions():

    base = load_base(set_terms=True, set_excl=True)

    base.unload_exclusions()

    assert not base.exclusions

# def test_set_terms():

#     base = load_base()
#     base.set_terms(['think', 'do'])

#     assert base.terms

# def test_set_terms_file_cog():
#     """Test the set_terms_file method of Base(), for cognitive files."""

#     base = load_base()
#     base.set_terms_file('cognitive')

#     assert base.terms

# def test_set_terms_file_dis():
#     """Test the set_terms_file method of Base(), for disease files."""

#     base = load_base()
#     base.set_terms_file('disease')

#     assert base.terms

# def test_check_terms():
#     """Test the check_terms method of Base()."""

#     base = load_base(set_terms='cognitive')

#     base.check_terms()

#     assert True

# def test_unload_terms():
#     """Test the unload_terms method of Base()."""

#     base = load_base(set_terms='disease')

#     base.unload_terms()

#     assert not base.terms_type
#     assert not base.terms
#     assert not base.n_terms

# def test_get_db_info():
#     """Test the get_db_info method of Base()."""

#     base = load_base()

#     base.get_db_info('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=pubmed')

#     assert base.db_info
