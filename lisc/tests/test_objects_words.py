"""Tests for the Words() class and related functions from lisc."""

from py.test import raises

#import requests
#import bs4
#from bs4 import BeautifulSoup

from lisc.data import Data
from lisc.objects.words import Words

###################################################################################################
###################################################################################################

def test_words():

    assert Words()

def test_get_item():

    words = Words()

    # Test error for empty object
    with raises(IndexError):
        words['not a thing']

    words.add_results(Data('test', ['test']))

    # Test error for wrong key
    with raises(IndexError):
        words['wrong']

    # Test properly extracting item
    assert words['test']

def test_add_results():

    words = Words()

    words.add_results(Data(['test']))

    assert words.results

def test_run_scrape():

    words = Words()

    words.add_terms(['language', 'memory'])
    words.add_terms(['protein', ''], 'exclusions')

    words.run_scrape(db='pubmed', retmax='2')

    assert words.results
    assert words.labels
