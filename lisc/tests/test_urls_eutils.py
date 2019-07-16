"""Tests for EUtils URL functions and classes for lisc."""

from py.test import raises

from lisc.urls.eutils import *

###################################################################################################
###################################################################################################

def test_get_wait_time():

    assert get_wait_time(True)

def test_eutils():

    assert EUtils()

def test_urls_settings():
    """Tests URLS() returns properly with settings provided, and args defined."""

    urls = EUtils(db='pubmed', retmax=500, retmode='xml')
    assert urls.settings['db'] == 'pubmed'
    assert urls.settings['retmax'] == '500'
    with raises(KeyError):
        urls.settings['field']

def test_build_url():

    urls = EUtils(db='pubmed', retmax='500', field='id', retmode='xml')

    urls.build_url('info', [])
    assert urls.utils['info']

    urls.build_url('query', ['db'])
    assert urls.utils['query']

    urls.build_url('search', ['db', 'retmode'])
    assert urls.utils['search']

    urls.build_url('fetch', ['db', 'retmode'])
    assert urls.utils['fetch']

def test_get_url():

    urls = EUtils(db='pubmed', retmode='xml')

    urls.build_url('info', ['db'])
    info = urls.get_url('info')
    assert 'info' in info

    urls.build_url('fetch', ['db', 'retmode'])
    fetch = urls.get_url('fetch', {'WebEnv' : 'DATA'})
    assert 'fetch' in fetch
    assert 'WebEnv' in fetch
