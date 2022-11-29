"""Tests for lisc.urls.urls."""

from pytest import raises

from lisc.urls.urls import *

###################################################################################################
###################################################################################################

def test_urls():

    base = 'fake_base'
    utils = {'fake_util' : 'not_a_url'}

    assert URLs(base, utils)

def test_check_url():

    base = 'fake_base'
    utils = {'fake_util' : 'not_a_url'}

    urls = URLs(base, utils)

    urls.check_url('fake_util')
    with raises(ValueError):
        urls.check_url('wrong_name')

def test_fill_settings():

    urls = URLs('www.api.com', {'dostuff' : 'action'})
    urls.fill_settings(setting='val1', other='val2')

    assert urls.settings['setting'] == 'val1'
    assert urls.settings['other'] == 'val2'

def test_build_url():

    urls = URLs('www.api.com', {'dostuff' : 'action'})

    urls.build_url('dostuff', ['segment'], {'setting' : 'value'})

    assert urls.urls['dostuff'] == 'www.api.com/action/segment?setting=value'

def test_get_url():

    urls = URLs('www.api.com', {'dostuff' : 'action'})

    urls.build_url('dostuff')
    url = urls.get_url('dostuff', ['segment'], {'setting' : 'value'})
    url = 'www.api.com/action/segment?setting=value'
