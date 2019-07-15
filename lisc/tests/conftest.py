""""Configuration file for pytest, for testing LISC."""

import pytest

import os
import shutil
import pkg_resources as pkg

import nltk

from lisc.objects import Counts, Words
from lisc.requester import Requester
from lisc.core.modutils import safe_import
from lisc.core.db import create_file_structure
from lisc.tests.utils import create_files, load_base, load_data, load_data_all
from lisc.tests.utils import TestDB as TDB

plt = safe_import('.pyplot', 'matplotlib')

###################################################################################################
###################################################################################################

def pytest_configure(config):

    # Set backend for matplotlib tests, if mpl is available
    if plt:
        plt.switch_backend('agg')

@pytest.fixture(scope='session', autouse=True)
def download_data():

    # Download required nltk data for tokenizing
    nltk.download('punkt')
    nltk.download('stopwords')

@pytest.fixture(scope='session', autouse=True)
def check_db():
    """Once, prior to session, this will clear and re-initialize the test file database."""

    # Create the test database directory
    test_db_dir = pkg.resource_filename(__name__, 'test_db')

    # If the directories already exist, clear them
    if os.path.exists(test_db_dir):
        shutil.rmtree(test_db_dir)

    create_file_structure(test_db_dir)
    create_files(os.path.join(test_db_dir, 'Terms'))

@pytest.fixture(scope='session')
def tdb():
    return TDB()

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
def tbase_empty():
    return load_base()

@pytest.fixture(scope='function')
def tbase_terms():
    return load_base(True)

@pytest.fixture(scope='function')
def tbase_terms_excl():
    return load_base(True, True)

@pytest.fixture(scope='function')
def tdata_empty():
    return load_data()

@pytest.fixture(scope='function')
def tdata_full():
    return load_data(add_dat=True, n_dat=2)

@pytest.fixture(scope='function')
def tdata_all():
    return load_data_all()
