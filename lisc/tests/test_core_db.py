"""Tests for the database classes and functions from lisc.core."""

from lisc.core.db import *

###################################################################################################
###################################################################################################

def test_SCDB():

    db = SCDB(auto_gen=False)
    assert db

    db.gen_paths()
    assert db

def test_check_folder():

    assert check_folder(None, '') == ''
    assert check_folder('string', '') == 'string'
    assert isinstance(check_folder(SCDB(), 'terms'), str)
