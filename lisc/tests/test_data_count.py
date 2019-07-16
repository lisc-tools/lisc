"""Tests for the data count from lisc."""

from lisc.data.count import *
from lisc.data.count import _fix_author_names

###################################################################################################
###################################################################################################

def test_count_years():

    tdat = [1991, 1991, 1995, 2000]
    out = count_years(tdat)

    assert out == [(1991, 2), (1995, 1), (2000, 1)]

def test_count_journals():

    tdat = [('J. Python', 'JP'), ('Journal of Software Testing', 'JST'), ('J. Python', 'JP')]
    out = count_journals(tdat)

    assert out == [(2, 'J. Python'), (1, 'Journal of Software Testing')]

def test_count_authors():

    tdat = [[('Smith', 'Alfred', 'AS', 'Python'),
             ('Doe', 'Jane', 'JR', 'JavaScript')],
            [('Smith', 'Alfred', 'AS', 'Python')]]

    out = count_authors(tdat)

    assert out == [(2, ('Smith', 'AS')), (1, ('Doe', 'JR'))]

def test_count_end_authors():

    tdat = [[('Smith', 'Alfred', 'AS', 'Python'),
             ('Middle', 'Arthur', 'AA', 'Matlab'),
             ('Doe', 'Jane', 'JR', 'JavaScript')],
            [('Smith', 'Alfred', 'AS', 'Python')]]

    f_authors, l_authors = count_end_authors(tdat)

    assert f_authors == [(2, ('Smith', 'AS'))]
    assert l_authors == [(1, ('Doe', 'JR'))]

def test_fix_author_names():

    tdat = [('Smith', 'AS'), (None, None), ('Doe', 'JR')]

    out = _fix_author_names(tdat)

    assert out == [('Smith', 'AS'), ('Doe', 'JR')]
