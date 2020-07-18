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

    settings = make_settings({'setting' : 'val1', 'other' : 'val2'})
    assert settings[0] == '?'
    assert 'setting=val1' in settings
    assert 'other=val2' in settings
    assert make_settings({}) == ''
