"""Tests for the database classes and functions from lisc.core."""

import os

from lisc.core.db import *

###################################################################################################
###################################################################################################

def test_SCDB():

    assert SCDB(auto_gen=False)

def test_SCDB_gen_paths():

    db = SCDB(auto_gen=False)
    db.gen_paths()

    assert db

# def test_SCDB_paths():
#     """Test that all defined SCDB paths exist."""

#     db = SCDB()

#     # Loops through all paths, checking they exist
#     #  Skips vars without '_path' marker, and empty variables
#     for key, val in vars(db).items():
#         if '_path' in key and val:
#             assert os.path.exists(val)

def test_webdb():

    assert WebDB()

# def test_webdb_paths():
#     """Test that all defined WebDB paths exist."""

#     db = WebDB()

#     # Loops through all paths, checking they exist
#     #  Skips vars without '_path' marker, and empty variables
#     for key, val in vars(db).items():
#         if '_path' in key and val:
#             assert os.path.exists(val)

def test_check_folder():

    assert check_folder(None, '') == None
    assert check_folder('string', '') == 'string'
    assert isinstance(check_folder(SCDB(), 'terms'), str)
    #assert isinstance(check_folder(SCDB(), 'terms'), SCDB)
