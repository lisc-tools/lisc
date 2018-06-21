"""Tests for URL functions and classes from lisc.core."""

from py.test import raises

from lisc.core.urls import URLS
from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

def test_urls():
    """Test the URLS object returns properly."""

    assert URLS(auto_gen=False)
    assert URLS(auto_gen=True)

def test_urls_settings_args():
    """Tests URLS() returns properly with settings provided, and args defined.
    This triggers save_settings() and save_args() methods with inputs from __init__.
    """

    assert URLS(db='pubmed', retmax='500', field='id', retmode='xml')

def test_check_args():
    """Test the check_args() method from URLS()."""

    urls = URLS(db='pubmed', field='id')

    urls.check_args(['db', 'field'])

    # Check error
    with raises(InconsistentDataError):
        urls.check_args(['db', 'retmax', 'field'])

def test_build_info():
    """Test the build_info() method from URLS()."""

    urls = URLS()

    urls.build_info([])

    assert urls.info

def test_build_query():
    """Test the build_query() method from URLS()."""

    urls = URLS(db='pubmed')

    urls.build_query(['db'])

    assert urls.query

def test_build_search():
    """Test the buid_search() method form URLS()."""

    urls = URLS(db='pubmed', retmax='500', field='id', retmode='xml')

    urls.build_search(['db', 'retmode'])

    assert urls.search

def test_build_fetch():
    """Test the build_fetch() method from URLS()."""

    urls = URLS(db='pubmed', retmax='500', field='id', retmode='xml')

    urls.build_fetch(['db', 'retmode'])

    assert urls.fetch
