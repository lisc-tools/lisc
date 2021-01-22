"""Tests for lisc.collect.process."""

from py.test import raises

import bs4

from lisc.collect.process import *

###################################################################################################
###################################################################################################

def test_extract():

    # Create a complex tag
    out = bs4.element.Tag(name='Out')
    inn1 = bs4.element.Tag(name='Inn')
    inn2 = bs4.element.Tag(name='Inn')

    inn1.append('words words')
    inn2.append('more words')

    out.append(inn1)
    out.append(inn2)

    # Test error with a bad 'how' input
    with raises(ValueError):
        out_err = extract(out, 'Inn', 'bad')

    # Test with how = 'raw'
    out_raw = extract(out, 'Inn', 'raw')
    assert type(out_raw) is bs4.element.Tag

    # Test with how = 'str'
    out_str = extract(out, 'Inn', 'str')
    assert isinstance(out_str, str)
    assert out_str == 'words words'

    # Test with how = 'all'
    out_all = extract(out, 'Inn', 'all')
    assert type(out_all) is bs4.element.ResultSet

    # Test with non-existent tag name
    out_none = extract(out, 'bad', 'raw')
    assert out_none is None

def test_ids_to_str():

    idd = bs4.element.Tag(name='id')
    idd.append('1111')
    ids = bs4.element.ResultSet(source=None, result=(idd, idd))

    out = ids_to_str(ids)

    assert out == '1111,1111'

def test_none_process():
    """Test the decorator on '_process' functions that catches & return None inputs."""

    # None inputs should give a None output
    assert process_authors(None) is None
    assert process_pub_date(None) is None
    assert process_ids(None, 'doi') is None
