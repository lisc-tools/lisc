"""
Tutorial 04: Counts Analysis
============================

Analyzing collected co-occurrence data.
"""

###################################################################################################
# Counts Analyses
# ---------------
#
# This tutorial explores analyzing collected co-occurrence data.
#
# Note that this tutorials requires some optional dependencies, including
# matplotlib, seaborn and scipy.
#

###################################################################################################

# Import database and IO utilities to reload our previously collected data
from lisc.utils.db import SCDB
from lisc.utils.io import load_object

# Import plots that are available for co-occurrence analysis
from lisc.plts.counts import plot_matrix, plot_clustermap, plot_dendrogram

###################################################################################################

# Reload the counts object from the last tutorial
counts = load_object('tutorial_counts', SCDB('lisc_db'))

###################################################################################################
#
# The :class:`~.Counts` object has some helper methods to explore the collected data.
#
# First lets check the number of counts per term list, which we can do with the
# :meth:`~.Counts.check_data` method.
#

###################################################################################################

# Look at the collected counts data for the first set of terms
counts.check_data(data_type='counts', dim='A')

###################################################################################################

# Look at the collected counts data for the second set of terms
counts.check_data(data_type='counts', dim='B')

###################################################################################################
# Normalization & Scores
# ----------------------
#
# The collected co-occurrence data includes information on the number of articles in which
# terms co-occur, as well as the number of articles for each term independently.
#
# Once we have this data, we typically want to calculate a normalized measures,
# and/or other kinds of similarity score, to compare between terms.
#
# To normalize the data, we can divide the co-occurrence counts by the number of articles
# per term. This allows us the examine, for example, the proportion of articles
# that include particular co-occurrence patterns.
#
# These measures are available using the :meth:`~.Counts.compute_score` method. This method
# can compute different types of scores, with the type specified by  the first input to the
# method. Scores available include 'normalize', 'association', or 'similarity'.
#

###################################################################################################

# Compute a normalization of the co-occurrence data
counts.compute_score('normalize', dim='A')

###################################################################################################

# Check out the computed normalization
print(counts.score)

###################################################################################################
#
# The normalization is the number of articles with both terms, divided by the number of
# articles for a single term. It can therefore be interpreted as a proportion of articles
# with term `a` that also have term `b`, or as `a & b / a`.
#
# Note that when using two different terms lists, you have to choose which list of
# terms to normalize by, which is controlled by the `dim` input.
#
# In this case, we have calculated the normalized data as the proportion of
# articles for each anatomical term that include each perception term.
#
# Alternately, we can also calculate an association index or score, as below:
#

###################################################################################################

# Compute the association index
counts.compute_score('association')

###################################################################################################

# Check out the computed score
print(counts.score)

###################################################################################################
#
# Specifying 'association' computes the
# `Jaccard index <https://en.wikipedia.org/wiki/Jaccard_index>`_,
# which is a standard measure for measuring the similarity of samples, calculating
# a normalized measure of similarity, bounded between 0 and 1.
#
# One benefit of the Jaccard index is that you do not have to choose a terms list to normalize
# by - the calculated measure considers both lists of terms to compute an association index.
#
# The cosine similarity of the co-occurrence data can also be calculated, with 'similarity'.
#

###################################################################################################
# Clustering and Plotting Co-occurrence Data
# ------------------------------------------
#
# The collected co-occurrence data is a 2D matrix of counts reflecting the relationship
# between terms. This makes it amenable to visualizations and analyses, such as clustering,
# that look to find structure in the data.
#
# LISC provides some functions to visualize and cluster co-occurrence data. These functions
# use functionality offered by optional dependencies, including scipy and seaborn, which
# need to be installed for these to run.
#
# The functions :func:`~.plot_matrix`, :func:`~.plot_clustermap`, and :func:`~.plot_dendrogram`
# offer visualizations and clustering. You can check through each function for details on what
# each one is doing.
#

###################################################################################################

# Plot a matrix of the association index data
plot_matrix(counts, attribute='score')

###################################################################################################

# Plot a clustermap of the association index data
plot_clustermap(counts, attribute='score')

###################################################################################################

# Plot a dendrogram, to cluster the terms
plot_dendrogram(counts, attribute='score')
