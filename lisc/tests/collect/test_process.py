"""Tests for lisc.collect.process."""

from pytest import raises

import bs4

from lisc.collect.process import *

###################################################################################################
###################################################################################################

def test_get_info(ttag):

    # Test error with a bad 'how' input
    with raises(ValueError):
        out_err = get_info(ttag, 'Inn1', 'bad')

    # Test with how = 'raw'
    out_raw = get_info(ttag, 'Inn1', 'raw')
    assert type(out_raw) is bs4.element.Tag

    # Test with how = 'str'
    out_str = get_info(ttag, 'Inn1', 'str')
    assert isinstance(out_str, str)
    assert out_str == 'words words'

    # Test with how = 'all'
    out_all = get_info(ttag, 'Inn1', 'all')
    assert type(out_all) is bs4.element.ResultSet

    # Test with non-existent tag name
    out_none = get_info(ttag, 'bad', 'raw')
    assert out_none is None

def test_extract_tag_first(ttag):

    # Test extracting first tag, if it exists
    _, extracted = extract_tag(ttag, 'Inn1', 'first')
    assert isinstance(extracted, bs4.element.Tag)

    # Test extracting first tag, if it doesn't exist
    _, extracted = extract_tag(ttag, 'NotInn', 'first')
    assert extracted is None

    # Test error if attribute not found
    with raises(AttributeError):
        _, extracted = extract_tag(ttag, 'Bad', 'first', True)

def test_extract_tag_all(ttag):

    # Test extracting all tags
    _, extracted_all = extract_tag(ttag, 'Inn1', 'all')
    assert isinstance(extracted_all, list)
    assert len(extracted_all) == 2

    # Test error if attribute not found
    with raises(AttributeError):
        _, extracted = extract_tag(ttag, 'Bad', 'all', True)

def test_none_process():
    """Test the decorator on '_process' functions that catches & return None inputs."""

    # None inputs should give a None output
    assert process_authors(None) is None
    assert process_pub_date(None) is None
    assert process_ids(None, 'doi') is None
