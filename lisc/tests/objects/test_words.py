"""Tests for lisc.objects.words"""

from py.test import raises

from lisc.data import Term, Articles
from lisc.objects.words import Words

###################################################################################################
###################################################################################################

def test_words():

    assert Words()

def test_get_item(tterm):

    words = Words()

    # Test error for empty object
    with raises(IndexError):
        words['not a thing']

    words.add_results(Articles(tterm))

    # Test error for wrong key
    with raises(IndexError):
        words['wrong']

    # Test properly extracting item
    arts = words[tterm.label]
    assert isinstance(arts, Articles)

def test_add_results(tterm):

    words = Words()

    words.add_results(Articles(tterm))

    assert words.results

def test_collect(test_req):

    words = Words()

    terms = ['language', 'memory']
    excls = ['protein', '']
    words.add_terms(terms)
    words.add_terms(excls, 'exclusions')

    retmax = 2
    words.run_collection(db='pubmed', retmax=retmax, logging=test_req)
    assert words.has_data
    assert len(words.results) == len(terms)

    check_dunders(words)
    check_funcs(words)
    drop_data(words, retmax+1)

def check_dunders(words):

    for ind, result in enumerate(words):
        ind += 1
        assert result
    assert ind == len(words.results)

def check_funcs(words):

    words.check_data()

def drop_data(words, n_articles):

    words.drop_data(n_articles)
    assert words.n_terms == len(words.results) == 0
