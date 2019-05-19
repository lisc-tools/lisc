"""Tests for the basic utilities functions from lisc.core."""

from py.test import raises

import bs4

from lisc.core.utils import comb_terms, extract

###################################################################################################
###################################################################################################

def test_comb_terms():

    out = comb_terms(['one', 'two'], 'or')
    assert out == '("one"OR"two")'

    out = comb_terms(['one', 'two'], 'not')
    assert out == 'NOT"one"NOT"two"'


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
    #TODO: Figure this out? Whats the return type?
    #assert isinstance(out_str, str)
    #assert out_str == 'words words'

    # Test how = 'all'
    out_all = extract(out, 'Inn', 'all')
    assert type(out_all) is bs4.element.ResultSet

    # Test with non-existent tag name
    out_none = extract(out, 'bad', 'raw')
    assert out_none is None
