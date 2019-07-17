"""
Tutorial 02 - Counts Analysis
=============================

Analyzing scraped co-occurence data.
"""

from lisc import SCDB, load_object


from lisc.plts.group import *

###################################################################################################
#
# Counts Analyses
# ---------------
#
# This tutorial explores the built in utilities for exploring & anayzing counts data.
#

counts = load_object('tutorial_counts', SCDB('lisc_db'))



###################################################################################################

counts.check_data(data_type='counts', dim='A', )

###################################################################################################

counts.check_data(data_type='counts', dim='B', )

###################################################################################################
#
# Scores
# ------
#
# The Counts co-occurence data collection gives us a raw data matrix of the number of
# papers in with terms co-occur, as well as counts of the number of total papers using
# each term.
#
#

###################################################################################################

# Compute the association index
counts.compute_score('association')

###################################################################################################

# Plot a matrix of the association index data
plot_matrix(counts.score, counts.terms['A'].labels, counts.terms['B'].labels)

###################################################################################################

# Plot a clustermap of the association index data
plot_clustermap(counts.score, counts.terms['A'].labels, counts.terms['B'].labels)

###################################################################################################

# Plot a dendrogram, to cluster the terms
plot_dendrogram(counts.score, counts.terms['B'].labels)

###################################################################################################
