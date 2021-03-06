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

    compute_scores(counts)
    check_funcs(counts)
    drop_data(counts)

def test_collect_two():

    counts = Counts()

    counts.add_terms(['language', 'memory'], dim='A')
    counts.add_terms(['protein', 'protein'], term_type='exclusions', dim='A')
    counts.add_terms(['cognition'], dim='B')

    counts.run_collection(db='pubmed')
    counts.compute_score('normalize')

    compute_scores(counts)
    check_funcs(counts)
    drop_data(counts)

def compute_scores(counts):

    for score_type in ['normalize', 'association', 'similarity']:
        counts.compute_score(score_type)
        assert counts.score.any()
        assert counts.score_info['type'] == score_type

def check_funcs(counts):

    counts.check_data()
    counts.check_top()
    counts.check_counts()

def drop_data(counts):

    counts.drop_data(0)
