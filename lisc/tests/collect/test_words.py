"""Tests for lisc.collect.words."""

import requests
from bs4 import BeautifulSoup

from lisc.collect.words import *

###################################################################################################
###################################################################################################

def test_collect_words(tdb, test_req):

    terms = [['science'], ['engineering']]
    excls = [['philosophy'], []]
    retmax = 2

    # Test without using history, and without saving & clearing
    res, meta_data = collect_words(terms, excls, db='pubmed', retmax=retmax, save_and_clear=False,
                                   usehistory=False, logging=test_req)
    assert len(res) == len(terms)
    assert meta_data['requester']['n_requests'] > 0
    assert res[0].n_articles == retmax
    for field in ['titles', 'authors', 'ids', 'journals', 'keywords', 'words', 'years']:
        assert getattr(res[0], field)

def test_collect_words_history(tdb, test_req):

    terms = [['science'], ['engineering']]
    excls = [['philosophy'], []]
    retmax = 2

    # Test with using history, and with using save and clear
    res, meta_data = collect_words(terms, excls, db='pubmed', retmax=retmax, save_and_clear=True,
                                   usehistory=True, directory=tdb, logging=test_req)
    assert len(res) == len(terms)
    assert meta_data['requester']['n_requests'] > 0
    assert res[0].n_articles == 0
    for field in ['titles', 'authors', 'ids', 'journals', 'keywords', 'words', 'years']:
        assert getattr(res[0], field) == []

def test_get_article_info():

    arts = Articles('test')

    page = requests.get(("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
                         "efetch.fcgi?&db=pubmed&retmode=xml&id=28000963"))
    page_soup = BeautifulSoup(page.content, "xml")

    art = page_soup.findAll('PubmedArticle')[0]

    arts = get_article_info(arts, art)

    assert arts.ids[0] == '28000963'
    assert arts.titles[0] == ("A Neurocomputational Model of the N400"
                              " and the P600 in Language Processing.")
    assert arts.words[0][:13] == "Ten years ago"
    assert arts.keywords[0][0] == "Computational modeling"
    assert arts.years[0] == 2017
    assert arts.dois[0] == '10.1111/cogs.12461'

    # Check page with all fields missing - check error handling
    page = requests.get('http://www.google.com')
    arts = get_article_info(arts, page)

    assert arts.ids[1] == None
    assert arts.titles[1] is None
    assert arts.words[1] is None
    assert arts.keywords[1] is None
    assert arts.years[1] is None
    assert arts.dois[1] is None
