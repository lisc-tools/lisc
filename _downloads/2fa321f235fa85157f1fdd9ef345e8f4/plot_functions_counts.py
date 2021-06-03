"""
Counts with Functions
=====================

Collect word co-occurrence data, using a function oriented approach.
"""

###################################################################################################
# Function Approach: collect_counts
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The function for collecting co-occurrence data is :func:`~.collect_counts`.
#
# Given a list of search terms, this function handles all the requests to collect the data.
#

###################################################################################################

# Import function to collect data, and helper functions to analyze co-occurrence data
from lisc.collect import collect_counts
from lisc.analysis.counts import compute_normalization, compute_association_index

###################################################################################################

# Set some terms to search for
terms_a = [['protein'], ['gene']]
terms_b = [['heart'], ['lung']]

###################################################################################################

# Collect co-occurrence data across a single list of terms
coocs, term_counts, meta_dat = collect_counts(terms_a, db='pubmed', verbose=True)

###################################################################################################

# Check how many articles were found for each combination
print(coocs)

###################################################################################################

# Print out how many articles found for each term
for term, count in zip(terms_a, term_counts):
    print('{:12} : {}'.format(term[0], count))

###################################################################################################
#
# When given a single set of terms, the function collects counts of each term
# against every other term in the list.
#
# You can also specify different sets of terms to collect. In the example below,
# each term in list A is collected measuring co-occurrences with each term in list B.
#

###################################################################################################

# Collect co-occurrence data across two different lists of terms
coocs, term_counts, meta_dat = collect_counts(
    terms_a=terms_a, terms_b=terms_b, db='pubmed', verbose=True)

###################################################################################################
# Calculating Co-occurrence Scores
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Once co-occurrence data has been collected, we often want to compute a normalization
# or transform of the data.
#
# The :func:`~.compute_normalization`, :func:`~.compute_association_index`
# and :func:`~.compute_similarity` functions take in co-occurrence data as returned
# by the :func:`~.collect_counts` function.
#
# More details on the measures available in LISC are available in the :class:`~.Counts`
# tutorial. When using the functions approach, all implemented scores and transforms
# are available in `lisc.analysis`.
#

###################################################################################################

# Calculate the normalized data measure, normalizing the co-occurrences by the term counts
normed_coocs = compute_normalization(coocs, term_counts[0], dim='A')

# Check the computed score measure for the co-occurrence collection
print(normed_coocs)

###################################################################################################

# Compute the association index score, calculating the Jaccard index from the co-occurrences
score = compute_association_index(coocs, term_counts[0], term_counts[1])

# Check the computed score measure for the co-occurrence collection
print(score)

###################################################################################################
#
# From here, further analysis of collected co-occurrence data depends on the goal of the analysis.
#
# There are also plot functions available, as demonstrated in the Counts tutorial.
#
