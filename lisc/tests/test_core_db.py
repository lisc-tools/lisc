"""Tests for the database classes and functions from lisc.core."""

from lisc.core.db import *

###################################################################################################
###################################################################################################

def test_SCDB():

    db = SCDB(generate_paths=False)
    assert db

    db.gen_paths()
    assert db

    db.get_folder_path('base')
    db.get_file_path('base', 'test.txt')
    db.check_file_structure()

def test_check_directory():

    assert check_directory(None, '') == ''
    assert check_directory('string', '') == 'string'
    assert isinstance(check_directory(SCDB(), 'terms'), str)

def test_check_file_structure(tdb):

    check_file_structure(tdb.paths['base'])
