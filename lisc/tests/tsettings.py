"""Settings for LISC tests."""

import os
from pathlib import Path

###################################################################################################
###################################################################################################

# Define the name of the test database
TEST_DB_NAME = 'test_db'

# Test paths
TESTS_PATH = Path(os.path.abspath(os.path.dirname(__file__)))
TEST_DB_PATH = TESTS_PATH / TEST_DB_NAME

# Define the request wait time for running tests
TEST_WAIT_TIME = 1.0
