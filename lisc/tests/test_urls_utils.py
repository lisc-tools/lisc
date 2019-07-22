"""Tests for URL utilities for LISC."""

from lisc.urls.utils import *

###################################################################################################
###################################################################################################

def test_prepend():

    assert prepend('Test', '?') == '?Test'
    assert prepend('', '/') == ''

def test_make_segments():

    make_segments(['section', 'other']) == '/section/other'
    make_segments([]) == ''

def test_make_settings():

    make_settings({'setting' : 'val1', 'other' : 'val2'}) == '?setting=val1&other=val2'
    make_settings({}) == ''
