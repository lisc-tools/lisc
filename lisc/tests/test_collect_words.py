"""Tests for words collections."""

import requests
from bs4 import BeautifulSoup

from lisc.collect.words import *

###################################################################################################
###################################################################################################

def test_collect_words(tdb):

    terms = ['science', 'engineering']
    excls = ['philosophy', []]

    # Without history, nor save & clearing
    res, meta_data = collect_words(terms, excls, db='pubmed', retmax='2',
                                   save_and_clear=False, usehistory=False)
    assert res

    # With history, and using save and clear
    res, meta_data = collect_words(terms, excls, db='pubmed', retmax='2',
                                   usehistory=True, directory=tdb)
    assert res

def test_extract_add_info():

    data = Data('test')

    # Check page with all fields defined - check data extraction
    page = requests.get(("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
                         "efetch.fcgi?&db=pubmed&retmode=xml&id=28000963"))
    page_soup = BeautifulSoup(page.content, "xml")
    art = page_soup.findAll('PubmedArticle')[0]

    data = extract_add_info(data, 111111, art)

    assert data.ids[0] == 111111
    assert data.titles[0] == ("A Neurocomputational Model of the N400"
                              " and the P600 in Language Processing.")
    assert data.words[0][0] == "ten"
    assert data.keywords[0][0] == "computational modeling"
    assert data.years[0] == 2017
    assert data.dois[0] == '10.1111/cogs.12461'

    # Check page with all fields missing - check error handling
    page = requests.get('http://www.google.com')
    data = extract_add_info(data, 999999, page)

    assert data.ids[1] == 999999
    assert data.titles[1] is None
    assert data.words[1] is None
    assert data.keywords[1] is None
    assert data.years[1] is None
    assert data.dois[1] is None
