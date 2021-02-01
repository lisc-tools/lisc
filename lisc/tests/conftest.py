""""Configuration file for pytest."""

import pytest

import os
import shutil
import pkg_resources as pkg

from lisc.objects import Counts, Words
from lisc.requester import Requester
from lisc.core.modutils import safe_import
from lisc.utils.db import create_file_structure

from lisc.tests.tdata import create_term_files, create_api_files
from lisc.tests.tobjs import TestDB, load_base, load_arts, load_arts_all, load_tag

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

    # Create the test database directory
    tests_dir = pkg.resource_filename('lisc', 'tests')
    test_db_name = 'test_db'

    # If the directories already exist, clear them
    if os.path.exists(os.path.join(tests_dir, test_db_name)):
        shutil.rmtree(os.path.join(tests_dir, test_db_name))

    tdb = create_file_structure(tests_dir, test_db_name)

    create_term_files(tdb)
    create_api_files(tdb)

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
def treq():
    return Requester()

@pytest.fixture(scope='function')
def tbase():
    return load_base()

@pytest.fixture(scope='function')
def tbase_terms():
    return load_base(True, True)

@pytest.fixture(scope='function')
def tarts_empty():
    return load_arts()

@pytest.fixture(scope='function')
def tarts_full():
    return load_arts(add_data=True, n_data=2)

@pytest.fixture(scope='function')
def tarts_all():
    return load_arts_all()

@pytest.fixture(scope='function')
def ttag():
    return load_tag()
