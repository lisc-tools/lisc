"""Tests for lisc.objects.base."""

from pytest import raises

from lisc.data.term import Term
from lisc.objects.base import Base
from lisc.utils.base import flatten
from lisc.modutils.errors import InconsistentDataError

###################################################################################################
###################################################################################################

def test_base():

    assert Base()

def test_copy():

    tbase = Base()
    ntbase = tbase.copy()

    assert ntbase != tbase

def test_get_item(tbase_terms):

    out = tbase_terms['label0']
    assert isinstance(out, Term)
    assert out.label == 'label0'

def test_iter(tbase_terms):

    for term in tbase_terms:
        assert isinstance(term, Term)

def test_get_index(tbase_terms):

    ind = tbase_terms.get_index('label0')
    assert ind == 0

def test_get_term(tbase_terms):

    # Test accessing with index
    out1 = tbase_terms.get_term(0)
    assert isinstance(out1, Term)
    assert out1.label == 'label0'

    # Test accessing with label
    out2 = tbase_terms.get_term('label0')
    assert isinstance(out2, Term)
    assert out2.label == 'label0'

    # Check that the same element accessed in different ways is the same
    assert out1 == out2

def test_add_terms_list(tbase):

    terms = [['word'], ['thing', 'same']]
    tbase.add_terms(terms)
    assert tbase.terms == terms

    inclusions = [['need'], ['required']]
    tbase.add_terms(inclusions, 'inclusions')
    assert tbase.inclusions == inclusions

    exclusions = [['not'], ['this']]
    tbase.add_terms(exclusions, 'exclusions')
    assert tbase.exclusions == exclusions

    assert tbase.has_terms

def test_add_terms_str(tbase):

    terms = ['word', ['thing', 'same']]
    incls = ['need', 'required']
    excls = ['not', 'this']

    terms_expected = [['word'], ['thing', 'same']]
    incls_expected = [['need'], ['required']]
    excls_expected = [['not'], ['this']]

    tbase.add_terms(terms, 'terms')
    tbase.add_terms(incls, 'inclusions')
    tbase.add_terms(excls, 'exclusions')

    assert tbase.terms == terms_expected
    assert tbase.inclusions == incls_expected
    assert tbase.exclusions == excls_expected

    assert tbase.has_terms

def test_add_terms_append(tbase):

    terms1 = [['word'], ['thing', 'same']]
    terms2 = [['added']]

    tbase.add_terms(terms1)
    tbase.add_terms(terms2, append=True)

    assert tbase.n_terms == len(terms1) + len(terms2)
    assert tbase.terms[0] == terms1[0]
    assert tbase.terms[-1] == terms2[-1]

    assert tbase.has_terms

def test_add_terms_term(tbase, tterm):

    tbase.add_terms(tterm)
    assert tbase.labels[0] == tterm.label
    assert tbase.terms[0] == tterm.search
    assert tbase.inclusions[0] == tterm.inclusions
    assert tbase.exclusions[0] == tterm.exclusions

    # Test with 2 terms. Note second term needs a unique label
    tterm2 = Term(label='label2', search=['test2', 'synonym2'],
                  inclusions=['incl2', 'incl_synonym2'],
                  exclusions=['excl2', 'excl_synonym2'])

    terms = [tterm, tterm2]
    tbase.add_terms(terms)
    assert tbase.n_terms == len(terms)
    for ind, term in enumerate(terms):
        assert tbase.labels[ind] == terms[ind].label
        assert tbase.terms[ind] == terms[ind].search
        assert tbase.inclusions[ind] == terms[ind].inclusions
        assert tbase.exclusions[ind] == terms[ind].exclusions

def test_add_terms_file(tdb, tbase):

    tbase.add_terms('test_terms', directory=tdb)
    assert tbase.terms

    tbase.add_terms('test_inclusions', 'inclusions', directory=tdb)
    assert tbase.inclusions

    tbase.add_terms('test_exclusions', 'exclusions', directory=tdb)
    assert tbase.exclusions

    assert tbase.has_terms

def test_add_terms_dict(tbase):

    terms_dict = {
        'terms' : [['word'], ['thing', 'same']],
        'inclusions' : [['need'], ['required']],
        'exclusions' : [['not'], ['this']],
        'labels' : ['label0', 'label1'],
    }

    tbase.add_terms(terms_dict)

    assert tbase.terms == terms_dict['terms']
    assert tbase.inclusions == terms_dict['inclusions']
    assert tbase.exclusions == terms_dict['exclusions']
    assert tbase.labels == terms_dict['labels']

def test_add_labels(tbase):

    # Define test terms & labels
    labels = ['first', 'second']
    terms = ['word', 'thing']

    # Test explicitly added labels, alone
    tbase.add_labels(labels, check_consistency=False)
    assert tbase.labels == tbase._labels == labels

    # Clear object for next test
    tbase.unload_terms('all', False)

    # Test explicitly added labels, when terms are present
    tbase.add_terms(terms)
    tbase.add_labels(labels)
    assert tbase.labels == tbase._labels == labels

    # Clear object for next test
    tbase.unload_terms('all', False)

    # Test not adding labels, when terms are present
    tbase.add_terms(terms)
    assert tbase._labels == [None, None]
    assert tbase.labels == terms

def tests_check_terms(tbase_terms):

    tbase_terms.check_terms()
    tbase_terms.check_terms('inclusions')
    tbase_terms.check_terms('exclusions')

def test_drop_term(tbase_terms):

    n_terms = tbase_terms.n_terms
    tbase_terms.drop_term('label1')
    assert 'label1' not in tbase_terms.labels
    for attr in ['terms', '_labels', 'inclusions', 'exclusions']:
        assert len(getattr(tbase_terms, attr)) == n_terms - 1

def test_unload_terms(tbase_terms):

    tbase_terms.unload_terms('inclusions', reset=False)
    assert not tbase_terms.inclusions

    tbase_terms.unload_terms('exclusions', reset=True)
    assert len(tbase_terms.exclusions) == len(tbase_terms.terms)
    assert not flatten(tbase_terms.exclusions)

    tbase_terms.unload_terms('terms')
    assert not tbase_terms.terms
    assert not tbase_terms.n_terms

def test_unload_terms_all(tbase_terms):

    tbase_terms.unload_terms('all')
    assert not tbase_terms.inclusions
    assert not tbase_terms.exclusions
    assert not tbase_terms.terms
    assert not tbase_terms.n_terms
    tbase_terms._check_term_consistency()

def test_unload_labels(tbase_terms):

    tbase_terms.unload_labels()
    assert tbase_terms._labels == [None, None]

def test_make_search_term(tbase_terms):

    sterm1 = tbase_terms.make_search_term(0)
    assert isinstance(sterm1, str)
    for attr in ['search', 'inclusions', 'exclusions']:
        for el in getattr(tbase_terms.get_term(0), attr):
            assert el in sterm1

    sterm2 = tbase_terms.make_search_term(tbase_terms.labels[1])
    assert isinstance(sterm2, str)
    for attr in ['search', 'inclusions', 'exclusions']:
        for el in getattr(tbase_terms.get_term(tbase_terms.labels[1]), attr):
            assert el in sterm2

def test_set_joiners(tbase_terms):

    tbase_terms.set_joiners(search='AND', inclusions='AND', exclusions='AND')
    sterm1 = tbase_terms.make_search_term(0)
    assert '"test0"AND"synonym0"' in sterm1
    assert '"incl0"AND"incl_synonym0"' in sterm1
    assert '"excl0"AND"excl_synonym0"' in sterm1

    with raises(ValueError):
        tbase_terms.set_joiners(search='MAYBE')

def test_set_none_labels(tbase):

    tbase.terms = [['first'], ['second']]
    assert tbase._labels == []
    tbase._set_none_labels()
    assert tbase._labels == [None, None]

def test_check_term_consistency(tbase_terms):

    tbase_terms._check_term_consistency()

    tbase_terms.exclusions = ['need', 'required']
    tbase_terms._check_term_consistency()

    tbase_terms.exclusions = ['not', 'avoid']
    tbase_terms._check_term_consistency()

    tbase_terms._labels = ['label0', 'label1']
    tbase_terms._check_term_consistency()

    with raises(InconsistentDataError):
        tbase_terms.inclusions = ['need']
        tbase_terms._check_term_consistency()

    with raises(InconsistentDataError):
        tbase_terms.exclusions = ['not', 'avoid', 'bad']
        tbase_terms._check_term_consistency()

    with raises(InconsistentDataError):
        tbase_terms._labels = ['label1', 'label2', 'label3']
        tbase_terms._check_term_consistency()

def test_check_labels(tbase, tbase_terms):

    terms = [['search0'], ['search1']]
    tbase.terms = terms
    tbase._check_labels()
    tbase._labels == [None, None]

    tbase_terms._labels = ['label1', 'label2']
    tbase_terms._check_labels()

    # Test error with non-unique labels
    with raises(InconsistentDataError):
        tbase_terms._labels = ['label', 'label']
        tbase_terms._check_labels()

def test_check_clusions(tbase):

    terms = [['search0'], ['search1']]
    tbase.terms = terms

    tbase._check_clusions()
    assert len(tbase.inclusions) == len(terms)
    assert flatten(tbase.inclusions) == []
    assert len(tbase.exclusions) == len(terms)
    assert flatten(tbase.exclusions) == []
