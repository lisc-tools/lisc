"""Tests for lisc.data.articles_all."""

from lisc.data.articles_all import *
from lisc.data.articles_all import _count_authors, _count_end_authors, _fix_author_names

###################################################################################################
###################################################################################################

def test_articles_all(tarts_full):

    data_all = ArticlesAll(tarts_full)
    assert data_all

def test_check(tarts_all):

    tarts_all.check_frequencies(data_type='words')
    tarts_all.check_frequencies(data_type='keywords')

def test_summary(tdb, tarts_all):

    tarts_all.create_summary()

    assert tarts_all.summary

    tarts_all.print_summary()
    tarts_all.save_summary(directory=tdb)

def test_count_authors():

    tdata = [[('Smith', 'Alfred', 'AS', 'Python'),
              ('Doe', 'Jane', 'JR', 'JavaScript')],
             [('Smith', 'Alfred', 'AS', 'Python')]]
    out = _count_authors(tdata)

    assert out[('Smith', 'AS')] == 2
    assert out[('Doe', 'JR')] == 1

def test_count_end_authors():

    tdata = [[('Smith', 'Alfred', 'AS', 'Python'),
              ('Middle', 'Arthur', 'AA', 'Matlab'),
              ('Doe', 'Jane', 'JR', 'JavaScript')],
             [('Smith', 'Alfred', 'AS', 'Python')]]

    f_authors, l_authors = _count_end_authors(tdata)

    assert f_authors[('Smith', 'AS')] == 2
    assert l_authors[('Doe', 'JR')] == 1

def test_fix_author_names():

    tdata = [('Smith', 'AS'), (None, None), ('Doe', 'JR'), ('First Middle Last', None)]
    out = _fix_author_names(tdata)

    assert out[0] == ('Smith', 'AS')
    assert out[1] == ('Doe', 'JR')
    assert None not in out
    assert out[-1] == ('Last', 'FM')
