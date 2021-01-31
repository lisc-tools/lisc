"""Tests for lisc.collect.process."""

from py.test import raises

import bs4

from lisc.collect.process import *

###################################################################################################
###################################################################################################

def test_get_info():

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
        out_err = get_info(out, 'Inn', 'bad')

    # Test with how = 'raw'
    out_raw = get_info(out, 'Inn', 'raw')
    assert type(out_raw) is bs4.element.Tag

    # Test with how = 'str'
    out_str = get_info(out, 'Inn', 'str')
    assert isinstance(out_str, str)
    assert out_str == 'words words'

    # Test with how = 'all'
    out_all = get_info(out, 'Inn', 'all')
    assert type(out_all) is bs4.element.ResultSet

    # Test with non-existent tag name
    out_none = get_info(out, 'bad', 'raw')
    assert out_none is None

def test_extract_tag_first():

    # Create a complex tag
    out = bs4.element.Tag(name='Out')
    inn1a = bs4.element.Tag(name='Inn1')
    inn1b = bs4.element.Tag(name='Inn1')

    inn1a.append('words words')
    inn1b.append('more words')

    out.append(inn1a)
    out.append(inn1b)

    # Test extracting first tag, if it exists
    _, extracted = extract_tag(out, 'Inn1', 'first')
    assert isinstance(extracted, bs4.element.Tag)

    # Test extracting first tag, if it doesn't exist
    _, extracted = extract_tag(out, 'NotInn', 'first')
    assert extracted is None

    # Test error if attribute not found
    with raises(AttributeError):
        _, extracted = extract_tag(out, 'Bad', 'first', True)

def test_extract_tag_all():

    # Create a complex tag
    out = bs4.element.Tag(name='Out')
    inn1a = bs4.element.Tag(name='Inn1')
    inn1b = bs4.element.Tag(name='Inn1')

    inn1a.append('words words')
    inn1b.append('more words')

    out.append(inn1a)
    out.append(inn1b)

    # Test extracting all tags
    _, extracted_all = extract_tag(out, 'Inn1', 'all')
    assert isinstance(extracted_all, list)
    assert len(extracted_all) == 2

    # Test error if attribute not found
    with raises(AttributeError):
        _, extracted = extract_tag(out, 'Bad', 'all', True)

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
