"""
Counts with Functions
=====================

Collect word co-occurence data, using the underlying functions from LISC.
"""

###################################################################################################
#
# Function Approach: collect_counts
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The core function for collecting co-occurence data is the `collect_counts` function.
#
# Given a list of search terms, this function handles all the requests to collect the data.
#

###################################################################################################

# Import function to collect data, and helper functions to analyze co-occurence data
from lisc.collect import collect_counts
from lisc.analysis.counts import compute_normalization, compute_association_index

###################################################################################################

# Set some terms to search for
terms_a = [['protein'], ['gene']]
terms_b = [['heart'], ['lung']]

###################################################################################################

# Collect 'counts' (co-occurence data) - across a single list of terms
coocs, term_counts, meta_dat = collect_counts(terms_a, db='pubmed', verbose=True)

###################################################################################################

# Check how many papers were found for each combination
print(coocs)

###################################################################################################

# Print out how many papers found for each term
for term, count in zip(terms_a, term_counts):
    print('{:12} : {}'.format(term[0], count))

###################################################################################################
#
# When given a single set of terms, the function collects counts of each term
# against every other term in the list.
#
# You can also specify different sets of terms to collect. In the example below,
# each term in list A is collected measuring co-occurences with each term in list B.
#

###################################################################################################

# Collect 'counts' (co-occurence data) across two different lists of terms
coocs, term_counts, meta_dat = collect_counts(
    terms_a=terms_a, terms_b=terms_b, db='pubmed', verbose=True)

###################################################################################################
#
# Calculating Co-Occurence Scores
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Once the co-occurence data is collected, we often want to compute a normalization
# or transform of the data.
#
# Some more details on the measures available in LISC are available in the `Counts`
# tutorial. When using the functions approach, all implemented scores and transforms
# are available in `lisc.analysis`, as functions that take in our collected data.
#

###################################################################################################

# Calculate the normalized data measure, normalizing the co-occurences by the term counts
normed_coocs = compute_normalization(coocs, term_counts[0], dim='A')

# Check the computed score measure for the co-occurence collection
print(normed_coocs)

###################################################################################################

# Compute the association index score, calculating the Jaccard index from the co-occurences
score = compute_association_index(coocs, term_counts[0], term_counts[1])

# Check the computed score measure for the co-occurence collection
print(score)

###################################################################################################
#
# From here, further analysis of collected co-occurence data depends on the goal of the analysis.
#
# There are also plot functions available, same as demonstrated in the Counts tutorial.
#
