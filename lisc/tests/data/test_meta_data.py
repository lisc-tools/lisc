"""Tests for lisc.data.meta_data."""

from lisc.data.meta_data import *

###################################################################################################
###################################################################################################

def test_meta_data(treq):

    meta_data = MetaData()
    assert meta_data
    assert meta_data['date']

    meta_data.add_requester(treq)
    assert meta_data.requester

    meta_data.add_db_info({'db' : 'name'})
    assert meta_data.db_info
