"""
Example - XXX
=============

XXXX.
"""

###################################################################################################

from lisc.scrape import scrape_counts


###################################################################################################

terms_a = ['protein', 'gene']
terms_b = ['heart', 'lung']

###################################################################################################
#
# Running a scrape with the scrape_counts function
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Run a scrape of 'counts' (co-occurence data) - across a single list of terms
dat_numbers, dat_percent, term_counts, _, meta_dat = scrape_counts(terms_a, db='pubmed', verbose=True)


###################################################################################################

# Check how many papers were found for each combination
print(dat_numbers)

###################################################################################################

# Check out the percent of paper overlap
print(dat_percent)


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
dat_numbers, dat_percent, term_counts_a, term_counts_b, meta_dat = scrape_counts(
    terms_a=terms_a, terms_b=terms_b, db='pubmed', verbose=True)
