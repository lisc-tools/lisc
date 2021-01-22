"""Tests for lisc.objects.words"""

from py.test import raises

from lisc.data import Term, Articles
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

    words.add_results(Articles(Term('test', [], [], [])))

    # Test error for wrong key
    with raises(IndexError):
        words['wrong']

    # Test properly extracting item
    assert words['test']

def test_add_results():

    words = Words()

    words.add_results(Articles(Term('test', [], [], [])))

    assert words.results

def test_run_collection():

    words = Words()

    words.add_terms(['language', 'memory'])
    words.add_terms(['protein', ''], 'exclusions')

    words.run_collection(db='pubmed', retmax='2')

    assert words.results
    assert words.labels
