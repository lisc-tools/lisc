""""Configuration file for pytest, for testing lisc."""

import pytest

from lisc.tests.utils import load_base, load_data

###################################################################################################
###################################################################################################

@pytest.fixture(scope='function')
def tbase_empty():
    return load_base()

@pytest.fixture(scope='function')
def tbase_terms():
    return load_base(True)

@pytest.fixture(scope='function')
def tbase_terms_excl():
    return load_base(True, True)

@pytest.fixture(scope='function')
def tdata():
    return load_data()
