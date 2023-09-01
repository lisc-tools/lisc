"""Tests for lisc.data.process."""

from lisc.data.process import *
from lisc.data.process import _process_authors, _fix_author_names

###################################################################################################
###################################################################################################

def test_process_articles(tarts_data):

    arts = process_articles(tarts_data)

    # Check that data attributes maintain expected size
    for attr in ['words', 'years', 'authors', 'journals']:
        assert len(getattr(arts, attr)) == tarts_data.n_articles

    # Check that the processed attributes have correct types
    assert len(arts.authors[0]) == 2
    assert isinstance(arts.authors[0], list)
    assert isinstance(arts.authors[0][0], tuple)
    assert isinstance(arts.journals[0], str)
    assert isinstance(arts.words[0], list)

def test_process_with_none(tarts_none):

    arts = process_articles(tarts_none)
    for attr in ['words', 'years', 'authors', 'journals']:
        assert len(getattr(arts, attr)) == tarts_none.n_articles

def test_process_authors():

    tauthors = [[('Smith', 'Alfred', 'AS', 'Python'),
                 ('Doe', 'Jane', 'JR', 'JavaScript')],
                [('Smith', 'Alfred', 'AS', 'Python')]]
    out = _process_authors(tauthors)

    for ind in range(len(out)):
        assert len(out[ind]) == len(tauthors[ind])

    assert out[0] == [('Smith', 'AS'), ('Doe', 'JR')]
    assert out[1] == [('Smith', 'AS')]

def test_fix_author_names():

    tdata = [('Smith', 'AS'), (None, None), ('Doe', 'JR'), ('First Middle Last', None)]
    out = _fix_author_names(tdata)

    assert out[0] == ('Smith', 'AS')
    assert out[1] == ('Doe', 'JR')
    assert None not in out
    assert out[-1] == ('Last', 'FM')
