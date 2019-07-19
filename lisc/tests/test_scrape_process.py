"""Tests for the scrape process functions."""

from py.test import raises

import bs4

from lisc.scrape.process import *

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

    # Test error - bad how
    with raises(ValueError):
        out_err = extract(out, 'Inn', 'bad')

    # Test how = 'raw'
    out_raw = extract(out, 'Inn', 'raw')
    assert type(out_raw) is bs4.element.Tag

    # Test how = 'str'
    out_str = extract(out, 'Inn', 'str')
    assert isinstance(out_str, str)
    assert out_str == 'words words'

    # Test how = 'all'
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
    """The _process functions have a decorator to catch & return None inputs.
    Test that this is working - returns None when given None.
    """

    assert process_words(None) is None
    assert process_kws(None) is None
    assert process_authors(None) is None
    assert process_pub_date(None) == None
    assert process_ids(None, 'doi') == None

def test_process_words():

    words = 'The Last wOrd, in the eRp!'

    words_out = process_words(words)
    exp_out = ['last', 'word', 'erp']

    assert words_out == exp_out
