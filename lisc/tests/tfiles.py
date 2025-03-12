"""Utilities to create data files for testing."""

import os

from lisc.io.db import check_directory

###################################################################################################
###################################################################################################

def create_term_files(directory):
    """Creates some test term files."""

    path = check_directory(directory, 'terms')

    with open(os.path.join(path, 'test_terms.txt'), 'w') as term_file:
        term_file.write('word\nthing, same')

    with open(os.path.join(path, 'test_inclusions.txt'), 'w') as incl_file:
        incl_file.write('need\nrequired')

    with open(os.path.join(path, 'test_exclusions.txt'), 'w') as excl_file:
        excl_file.write('not\navoid')

    with open(os.path.join(path, 'test_exclusions_line.txt'), 'w') as excl_file2:
        excl_file2.write('not\n')

    with open(os.path.join(path, 'test_labels.txt'), 'w') as labels_file:
        labels_file.write('label1\nlabel2')


def create_api_files(directory):
    """Create test API key file."""

    path = check_directory(directory, 'base')

    with open(os.path.join(path, 'api_key.txt'), 'w') as term_file:
        term_file.write('123abc')
