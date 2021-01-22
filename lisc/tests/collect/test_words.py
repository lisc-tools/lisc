"""Tests for lisc.collect.words."""

import requests
from bs4 import BeautifulSoup

from lisc.collect.words import *

###################################################################################################
###################################################################################################

def test_collect_words(tdb):

    terms = ['science', 'engineering']
    excls = ['philosophy', []]

    # Test without using history, and without saving & clearing
    res, meta_data = collect_words(terms, excls, db='pubmed', retmax='2',
                                   save_and_clear=False, usehistory=False)
    assert res

    # Test with using history, and with using save and clear
    res, meta_data = collect_words(terms, excls, db='pubmed', retmax='2',
                                   usehistory=True, directory=tdb)
    assert res

def test_extract_add_info():

    arts = Articles('test')

    # Check page with all fields defined - check data extraction
    page = requests.get(("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
                         "efetch.fcgi?&db=pubmed&retmode=xml&id=28000963"))
    page_soup = BeautifulSoup(page.content, "xml")
    art = page_soup.findAll('PubmedArticle')[0]

    arts = extract_add_info(arts, 111111, art)

    assert arts.ids[0] == 111111
    assert arts.titles[0] == ("A Neurocomputational Model of the N400"
                              " and the P600 in Language Processing.")
    assert arts.words[0][:13] == "Ten years ago"
    assert arts.keywords[0][0] == "Computational modeling"
    assert arts.years[0] == 2017
    assert arts.dois[0] == '10.1111/cogs.12461'

    # Check page with all fields missing - check error handling
    page = requests.get('http://www.google.com')
    arts = extract_add_info(arts, 999999, page)

    assert arts.ids[1] == 999999
    assert arts.titles[1] is None
    assert arts.words[1] is None
    assert arts.keywords[1] is None
    assert arts.years[1] is None
    assert arts.dois[1] is None
