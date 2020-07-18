"""Tests for URL utilities for LISC."""

from lisc.urls.utils import *

###################################################################################################
###################################################################################################

def test_prepend():

    assert prepend('Test', '?') == '?Test'
    assert prepend('', '/') == ''

def test_make_segments():

    assert make_segments(['section', 'other']) == '/section/other'
    assert make_segments([]) == ''

def test_make_settings():

    assert make_settings({'setting' : 'val1', 'other' : 'val2'}) == '?setting=val1&other=val2'
    assert make_settings({}) == ''
