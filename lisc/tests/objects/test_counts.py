"""Tests for lisc.objects.counts."""

from lisc.objects.counts import Counts

###################################################################################################
###################################################################################################

def test_counts():

    assert Counts()

def test_collect_one():

    counts = Counts()

    counts.add_terms(['language', 'memory'], dim='A')
    counts.add_terms(['protein', 'protein'], term_type='exclusions', dim='A')

    counts.run_collection(db='pubmed')
    counts.compute_score('association')
    check_funcs(counts)
    drop_data(counts)

def test_collect_two():

    counts = Counts()

    counts.add_terms(['language', 'memory'], dim='A')
    counts.add_terms(['protein', 'protein'], term_type='exclusions', dim='A')
    counts.add_terms(['cognition'], dim='B')

    counts.run_collection(db='pubmed')
    counts.compute_score('normalize')
    check_funcs(counts)
    drop_data(counts)

def check_funcs(counts):

    counts.check_data()
    counts.check_top()
    counts.check_counts()

def drop_data(counts):

    counts.drop_data(0)
