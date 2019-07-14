"""Tests for URL functions and classes from lisc.core."""

from py.test import raises

from lisc.core.errors import InconsistentDataError

from lisc.urls.pubmed import *

###################################################################################################
###################################################################################################

def test_get_wait_time():

    assert get_wait_time(True)

def test_urls():

    assert URLS()

def test_urls_settings():
    """Tests URLS() returns properly with settings provided, and args defined.
    This triggers save_settings() and save_args() methods with inputs from __init__.
    """

    urls = URLS(db='pubmed', retmax=500, retmode='xml')
    assert urls.settings['db'] == 'pubmed'
    assert urls.settings['retmax'] == '500'
    with raises(KeyError):
        urls.settings['field']

def test_build_url():

    urls = URLS(db='pubmed', retmax='500', field='id', retmode='xml')

    urls.build_url('info', [])
    assert urls.info

    urls.build_url('query', ['db'])
    assert urls.query

    urls.build_url('search', ['db', 'retmode'])
    assert urls.search

    urls.build_url('fetch', ['db', 'retmode'])
    assert urls.fetch

def test_check_url():

    urls = URLS(db='pmc')
    urls.build_url('info', ['db'])

    urls.check_url('info')
    with raises(ValueError):
        urls.check_url('notinfo')

def test_get_url():

    urls = URLS(db='pubmed', retmode='xml')

    urls.build_url('info', ['db'])
    info = urls.get_url('info')
    assert 'info' in info

    urls.build_url('fetch', ['db', 'retmode'])
    fetch = urls.get_url('fetch', {'WebEnv' : 'DATA'})
    assert 'fetch' in fetch
    assert 'WebEnv' in fetch
