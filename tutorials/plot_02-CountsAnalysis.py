"""
Tutorial 02: Counts Analysis
============================

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

###################################################################################################

# Reload the counts object from the last tutorial
counts = load_object('tutorial_counts', SCDB('lisc_db'))

###################################################################################################
#
# The `Counts` object has some helper methods to explore the collected data.
#
# First lets check the number of counts per term list.
#

###################################################################################################

# Look at the collect counts data for the first set of terms
counts.check_data(data_type='counts', dim='A', )

###################################################################################################

# Look at the collect counts data for the second set of terms
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
# MORE INFORMATION ON SCORES
#

###################################################################################################

# Compute the association index
counts.compute_score('association')

###################################################################################################

# Check out the computed score
print(counts.score)

###################################################################################################
#
# Clustering and Plotting Counts Data
# -----------------------------------
#
# MORE INFORMATION HERE
#
# TODO: FIX UP PLOTS
#

###################################################################################################

# Plot a matrix of the association index data
plot_matrix(counts.score, counts.terms['B'].labels, counts.terms['A'].labels)

###################################################################################################

# Plot a clustermap of the association index data
plot_clustermap(counts.score, counts.terms['B'].labels, counts.terms['A'].labels)

###################################################################################################

# Plot a dendrogram, to cluster the terms
plot_dendrogram(counts.score, counts.terms['B'].labels)
