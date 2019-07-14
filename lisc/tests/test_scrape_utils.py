"""Tests for the scrape utilities."""

from lisc.scrape.utils import *

###################################################################################################
###################################################################################################

def test_join():

    assert join('Front', 'Back', '&&') == 'Front&&Back'
    assert join('', 'Back', '&&') == 'Back'
    assert join('Front', '', '&&') == 'Front'

def test_mk_term():

    assert mk_term(['word']) == '("word")'
    assert mk_term(['word', 'syn1']) == '("word"OR"syn1")'
    assert mk_term(['word', 'syn1', 'syn2']) == '("word"OR"syn1"OR"syn2")'
