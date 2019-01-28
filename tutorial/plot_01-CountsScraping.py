"""
Tutorial 01 - Counts Scraping
=============================
"""

###############################################################################
#
# This tutorial covers running scrapes, for count data.

###############################################################################
# Counts
# ------
#
# 'Counts' scrapes for co-occurence of given set(s) of terms.
#
# Running scrapes is available in both a 'functions' and 'objects' approach.
#

###############################################################################
#
# Set up some test data
#  Note that each entry is itself a list
terms_a = [['brain'], ['cognition']]
terms_b = [['body'], ['biology'], ['disease']]

###############################################################################
# Counts
# ------
#
# 'Counts' scraping gets data about the co-occurence of terms of interest.
#
# Specifically, it search titles and abstracts, and checks how often two terms of interest appear together in the literature.

# Import LISC - Count
from lisc.count import Count
from lisc.scrape import scrape_counts

###############################################################################
# Running a scrape with the scrape_counts function
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Run a scrape of 'counts' (co-occurence data) - across a single list of terms
dat_numbers, dat_percent, term_counts, _, meta_dat = scrape_counts(terms_a, db='pubmed', verbose=True)

###############################################################################

# Check out how many papers where found for each combination
print(dat_numbers)

###############################################################################

# Check out the percent of paper overlap
print(dat_percent)


###############################################################################

# Print out many papers found for each term
for term, count in zip(terms_a, term_counts):
    print('{:12} : {}'.format(term[0], count))

###############################################################################
#
# When given a single set of terms, the 'Counts' scrapes each term  against each other term.
#
# You can also specify different sets of terms to scrape, as below, whereby each term in list A is scraped for co-occurence for each term in list B (but not to other terms in list A).

###############################################################################

# Run a scrape of 'counts' (co-occurence data) across two different lists of terms
dat_numbers, dat_percent, term_counts_a, term_counts_b, meta_dat = scrape_counts(
    terms_lst_a=terms_a, terms_lst_b=terms_b, db='pubmed', verbose=True)


###############################################################################
# Count Object
# ------------
#
# There is also an OOP interface available in LISC, to organize the terms and data, and run scrapes.
#
# Note that the underlying code is the same - the count object ultimately calls the same scrape function as above.


###############################################################################

# Initialize counts object
counts = Count()

###############################################################################

# Set terms to run
counts.set_terms(terms_a)

###############################################################################

# Run scrape
counts.run_scrape(verbose=True)

###############################################################################
#
# The Counts object also comes with some helper methods to check out the data.

###############################################################################

# Check the highest associations for each term
counts.check_cooc()

###############################################################################

# Check how many papers were found for each search term
counts.check_counts()

###############################################################################

# Check the top term
counts.check_top()

###############################################################################
# Co-occurence data - different word lists

###############################################################################

# Initialize count object
counts_two = Count()

###############################################################################

# Set terms lists
#  Different terms lists are indexed by the 'A' and 'B' labels
counts_two.set_terms(terms_a, 'A')
counts_two.set_terms(terms_b, 'B')

###############################################################################

# Scrape co-occurence data
counts_two.run_scrape()

###############################################################################

# From there you can use all the same methods to explore the data
#  You can also specify which list to check
counts_two.check_cooc('A')
print('\n')
counts_two.check_cooc('B')

###############################################################################
# Synonyms & Exclusion Words
# --------------------------
#
# There is also support for adding synonyms and exclusion words.
#
# Synonyms are combined with the 'OR' operator, meaning results will be returned if they include any of the given terms.
#
# Exclusion words are combined with the 'NOT' operator, meaning entries will be excluded if they include these terms.
#
# For example, a using search terms ['gene', 'genetic'] with exclusion words ['protein'] creates the search:
# - ("gene"OR"genetic"NOT"protein")

###############################################################################

# Initialize Count object
counts = Count()

###############################################################################

# Set up terms with synonyms
#  Being able to include synonyms is the reason each term entry is itself a list
terms_lst = [['gene', 'genetic'], ['cortex', 'cortical']]

# Set up exclusions
#  You can also include synonyms for exclusions - which is why each entry is also a list
excl_lst = [['protein'], ['subcortical']]

# Set the terms & exclusions
counts.set_terms(terms_lst, 'A')
counts.set_exclusions(excl_lst, 'A')

###############################################################################

# You can check which terms are loaded
counts.terms['A'].check_terms()

###############################################################################

# Check exclusion words
counts.terms['A'].check_exclusions()

###############################################################################

# LISC objects will use the first item of each terms lists as a label for that term
counts.terms['A'].labels


###############################################################################
#
# Note that searching across different terms lists, and using synonyms and exclusions can all also be done directly using the scrape_counts function.
