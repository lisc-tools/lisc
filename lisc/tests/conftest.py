""""Configuration file for pytest."""

import pytest

import os
import shutil

from lisc.requester import Requester
from lisc.data.meta_data import MetaData
from lisc.io.db import create_file_structure
from lisc.modutils.dependencies import safe_import

from lisc.tests.tdata import create_term_files, create_api_files
from lisc.tests.tobjs import (TestDB, load_base, load_counts1d, load_counts, load_words,
                              load_arts, load_arts_all, load_tag, load_term, load_meta_dict)
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
def tcounts1d():
    return load_counts1d()

@pytest.fixture(scope='session')
def tcounts1d_data():
    return load_counts1d(add_terms=True, add_data=True)

@pytest.fixture(scope='session')
def tcounts():
    return load_counts()

@pytest.fixture(scope='session')
def tcounts_data():
    return load_counts(add_terms=True, add_data=True)

@pytest.fixture(scope='session')
def twords():
    return load_words()

@pytest.fixture(scope='function')
def twords_data():
    return load_words(add_terms=True, add_data=True)

@pytest.fixture(scope='function')
def treq():
    return Requester()

@pytest.fixture(scope='function')
def tbase():
    return load_base()

@pytest.fixture(scope='function')
def tbase_terms():
    return load_base(add_terms=True, add_clusions=True, add_labels=True)

@pytest.fixture(scope='function')
def tarts():
    return load_arts()

@pytest.fixture(scope='function')
def tarts_data():
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
def tmetadict():
    return load_meta_dict()

@pytest.fixture(scope='function')
def ttag():
    return load_tag()
