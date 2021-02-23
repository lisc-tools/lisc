"""Tests for lisc.data.meta_data."""

from datetime import datetime

from lisc.data.meta_data import *

###################################################################################################
###################################################################################################

def test_meta_data():

    meta_data = MetaData()
    assert meta_data
    assert meta_data['date']

def test_meta_data_get_date(tmetadata):

	tmetadata.get_date()
	assert isinstance(tmetadata.date, str)
	assert tmetadata.date[0:4] == str(datetime.now().year)

def test_meta_data_add_requester(treq)

    tmetadata.add_requester(treq)
    assert tmetadata.requester

def test_meta_data_add_db_info(tmetadata):

    tmetadata.add_db_info({'db' : 'name'})
    assert tmetadata.db_info

def test_meta_data_as_dict(tmetadata, treq):

	mt_dict = tmetadata.as_dict()
	assert isinstance(mt_dict, dict)

	# Test with db info added
	tmetadata.add_db_info({'db' : 'name'})

	# Test with a requester added
	tmetadata.add_requester(treq)
	mt_dict = tmetadata.as_dict()





