"""Tests for base URL functions and classes for lisc."""

from py.test import raises

from lisc.urls.urls import *

###################################################################################################
###################################################################################################

def test_urls():

    base = 'fake_base'
    utils = {'fake_util' : 'not_a_url'}

    assert URLS(base, utils)

def test_check_url():

    base = 'fake_base'
    utils = {'fake_util' : 'not_a_url'}

    urls = URLS(base, utils)

    urls.check_url('fake_util')
    with raises(ValueError):
        urls.check_url('wrong_name')
