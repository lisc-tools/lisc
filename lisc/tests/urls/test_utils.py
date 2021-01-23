"""Tests for lisc.urls.utils."""

from lisc.urls.utils import *

###################################################################################################
###################################################################################################

def test_check_none():

    out1 = check_none(None, 1)
    assert out1 == 1

    out2 = check_none(1, 2)
    assert out2 == 1

def test_check_settings():

    settings = {'key1' : 'value1', 'key2' : 12}
    output = check_settings(settings)
    for val in output.values():
        assert isinstance(val, str)

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
