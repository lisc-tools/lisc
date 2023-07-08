""""Configuration file for pytest."""

import pytest

import os
import shutil
from copy import deepcopy

from lisc.objects import Counts, Words
from lisc.requester import Requester
from lisc.data.meta_data import MetaData
from lisc.core.modutils import safe_import
from lisc.utils.db import create_file_structure

from lisc.tests.tdata import create_term_files, create_api_files
from lisc.tests.tobjs import TestDB, load_base, load_arts, load_arts_all, load_tag, load_term
from lisc.tests.tsettings import TEST_WAIT_TIME, TESTS_PATH, TEST_DB_PATH, TEST_DB_NAME

plt = safe_import('.pyplot', 'matplotlib')

###################################################################################################
###################################################################################################

def pytest_configure(config):

    # Set backend for matplotlib tests, if mpl is available
    if plt:
        plt.switch_backend('agg')

@pytest.fixture(scope='session', autouse=True)
def check_db():
    """Once, prior to session, this will clear and re-initialize the test file database."""

    # If the test directory already exists, clear it
    if os.path.exists(TEST_DB_PATH):
        shutil.rmtree(TEST_DB_PATH)

    tdb = create_file_structure(TESTS_PATH, TEST_DB_NAME)

    create_term_files(tdb)
    create_api_files(tdb)

@pytest.fixture(scope='function')
def test_req():
    return Requester(wait_time=TEST_WAIT_TIME)

@pytest.fixture(scope='session')
def tdb():
    return TestDB()

@pytest.fixture(scope='session')
def tcounts():
    return Counts()

@pytest.fixture(scope='session')
def twords():
    return Words()

@pytest.fixture(scope='function')
def twords_full():

    words = Words()
    arts = load_arts(add_data=True, n_data=2)
    words.results = [arts, deepcopy(arts)]

    return words

@pytest.fixture(scope='function')
def treq():
    return Requester()

@pytest.fixture(scope='function')
def tbase():
    return load_base()

@pytest.fixture(scope='function')
def tbase_terms():
    return load_base(True, True, True)

@pytest.fixture(scope='function')
def tarts_empty():
    return load_arts()

@pytest.fixture(scope='function')
def tarts_full():
    return load_arts(add_data=True, n_data=2)

@pytest.fixture(scope='function')
def tarts_none():
    return load_arts(add_data=True, n_data=2, add_none=True)

@pytest.fixture(scope='function')
def tarts_all():
    return load_arts_all()

@pytest.fixture(scope='session')
def tterm():
    return load_term()

@pytest.fixture(scope='function')
def tmetadata():
    return MetaData()

@pytest.fixture(scope='function')
def ttag():
    return load_tag()
