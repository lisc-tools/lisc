"""Tests for lisc.io.utils."""

from lisc.io.utils import *

###################################################################################################
###################################################################################################

def test_check_ext():

    assert check_ext('file', '.txt') == 'file.txt'
    assert check_ext('file.txt', '.txt') == 'file.txt'

def test_get_files(tdb):

    files = get_files(tdb.get_folder_path('terms'), drop_ext=True,
                      sort_files=True, drop_hidden=True, select='test')
    assert isinstance(files, list)
    assert isinstance(files[0], str)
