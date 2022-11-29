"""Tests for lisc.urls.eutils."""

from pytest import raises

from lisc.urls.eutils import *

###################################################################################################
###################################################################################################

def test_get_wait_time():

    assert get_wait_time(True)

def test_eutils():

    assert EUtils()

def test_urls_settings():

    urls = EUtils(db='database', retmax=500, retmode='xml')
    assert urls.settings['db'] == 'database'
    assert urls.settings['retmax'] == '500'
    with raises(KeyError):
        urls.settings['field']

def test_build_url():

    urls = EUtils(db='pubmed', retmax='500', field='id', retmode='xml')

    urls.build_url('info')
    assert urls.utils['info']

    urls.build_url('query', settings=['db'])
    assert urls.utils['query']

    urls.build_url('search', settings=['db', 'retmode'])
    assert urls.utils['search']

    urls.build_url('fetch', settings=['db', 'retmode'])
    assert urls.utils['fetch']

def test_get_url():

    urls = EUtils(db='pubmed', retmode='xml')

    urls.build_url('info', settings=['db'])
    info = urls.get_url('info')
    assert 'info' in info

    urls.build_url('fetch', settings=['db', 'retmode'])
    fetch = urls.get_url('fetch', {'WebEnv' : 'DATA'})
    assert 'fetch' in fetch
    assert 'WebEnv' in fetch
