"""Tests for URL functions and classes from lisc.core."""

from py.test import raises

from lisc.core.urls import URLS
from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

def test_urls():

    assert URLS()

def test_urls_settings_args():
    """Tests URLS() returns properly with settings provided, and args defined.
    This triggers save_settings() and save_args() methods with inputs from __init__.
    """

    assert URLS(db='pubmed', retmax='500', field='id', retmode='xml')

def test_check_args():

    urls = URLS(db='pubmed', field='id')

    urls.check_args(['db', 'field'])

    with raises(InconsistentDataError):
        urls.check_args(['db', 'retmax', 'field'])

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
