"""Tests for the single plots from lisc."""

import numpy as np

from lisc.tests.utils import plot_test, optional_test

from lisc.plts.single import *

###################################################################################################
###################################################################################################

@optional_test('matplotlib')
@plot_test
def test_plot_years():

    plot_years([(1900, 2), (2000, 2)])
