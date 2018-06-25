""""Configuration file for pytest, for testing lisc."""

import pytest

from lisc.tests.utils import load_base

###################################################################################################
###################################################################################################

@pytest.fixture(scope='function')
def tbase_empty():
    yield load_base()

@pytest.fixture(scope='function')
def tbase_terms():
    yield load_base(True)

@pytest.fixture(scope='function')
def tbase_terms_excl():
    yield load_base(True, True)

# @pytest.fixture(scope='session')
# def tfg():
#     yield get_tfg()