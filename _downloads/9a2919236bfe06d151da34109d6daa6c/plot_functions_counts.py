"""
Counts with Functions
=====================

Scraping word co-occurence data, using a function oriented approach.
"""

###################################################################################################
#
# Function Approach: collect_counts
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# MORE WORDS.
#

###################################################################################################

from lisc.collect import collect_counts
from lisc.analysis.counts import compute_association_index

###################################################################################################

# Set some terms lists
terms_a = [['protein'], ['gene']]
terms_b = [['heart'], ['lung']]

###################################################################################################

# Run a scrape of 'counts' (co-occurence data) - across a single list of terms
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
# When given a single set of terms, the 'Counts' scrapes each term  against each other term.
#
# You can also specify different sets of terms to scrape, as below, whereby
# each term in list A is scraped for co-occurence for each term in list B
# (but not to other terms in list A).
#

###################################################################################################

# Run a scrape of 'counts' (co-occurence data) across two different lists of terms
coocs, term_counts, meta_dat = collect_counts(
    terms_a=terms_a, terms_b=terms_b, db='pubmed', verbose=True)

###################################################################################################
#
# Calculating Scores
# ~~~~~~~~~~~~~~~~~~
#
#

###################################################################################################

# Compute the association index score
score = compute_association_index(coocs, term_counts[0], term_counts[1])

###################################################################################################

# Check the computed score measure for the co-occurence collection
print(score)
