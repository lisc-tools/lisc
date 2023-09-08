"""Tests for lisc.data.meta_data."""

from datetime import datetime

from lisc.data.meta_data import *

###################################################################################################
###################################################################################################

def test_meta_data():

    meta_data = MetaData()
    assert meta_data
    assert meta_data['date']

def test_meta_data_as_dict(tmetadata, treq):

    meta_dict = tmetadata.as_dict()
    assert isinstance(meta_dict, dict)

    # Test with db info added
    tmetadata.add_db_info({'dbname' : 'name'})
    meta_dict = tmetadata.as_dict()
    assert 'db_info_dbname' in meta_dict

    # Test with a requester added
    tmetadata.add_requester(treq)
    meta_dict = tmetadata.as_dict()
    assert 'requester_n_requests' in meta_dict

def test_meta_data_get_date(tmetadata):

    tmetadata.get_date()
    assert isinstance(tmetadata.date, str)
    assert tmetadata.date[0:4] == str(datetime.now().year)

def test_meta_data_add_requester(tmetadata, treq):

    tmetadata.add_requester(treq)
    assert tmetadata.requester

def test_meta_data_add_db_info(tmetadata):

    tmetadata.add_db_info({'dbname' : 'name'})
    assert tmetadata.db_info

def test_meta_data_add_settings(tmetadata):

    tmetadata.add_settings({'setting1' : 12, 'setting2' : True})
    assert tmetadata.settings

def test_meta_data_from_dict(tmetadict):

    meta_data = MetaData()
    meta_data.from_dict(tmetadict)
    for label in meta_data._dict_attrs:
        assert isinstance(getattr(meta_data, label), dict)

def test_meta_data_dict_managment(tmetadict):
    # Tests both `unpack` and `repack`

    meta_data = MetaData()

    repacked_dict = meta_data._repack_dict(tmetadict)
    assert isinstance(repacked_dict, dict)

    unpacked_dict = meta_data._unpack_dict(repacked_dict)
    assert isinstance(unpacked_dict, dict)

    assert unpacked_dict == tmetadict
