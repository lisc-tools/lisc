"""
Tutorial 03: Words Collection
=============================

Collecting literature data, extracting text and metadata for specified search terms.
"""

###################################################################################################
#
# Words
# -----
#
# Another way to scrape the literature is to collect text and meta-data from
# all papers found for a given set of terms.
#

###################################################################################################

from lisc import Words
from lisc import SCDB, save_object

###################################################################################################
#
# Words Object
# ------------
#
# The 'Words' object is used to collection and analyzing text data and article metadata.
#
# Search terms are specified to find papers of interest, from which text data and other
# information is collected.
#
# Note that the same approach for organizing search terms, including synonyms, inclusion
# and exclusion words, is used as for Counts, as described in the first tutorial.
#

###################################################################################################

# Set up some terms
terms = [['brain'], ['body']]

###################################################################################################

# Initialize Words object and set the terms to search for
words = Words()
words.add_terms(terms)

###################################################################################################

# Collect words data
words.run_collection(retmax='5')

###################################################################################################

# Words also saves the same list of Data objects
words.results

###################################################################################################
#
# Word Collections
# ----------------
#
# Depending on what the search terms are, collections of words papers can become quite large.
#
# Because of this, you might want to use some of the available EUtils settings, and
# LISC options to help control how the data collection is done.
#
# In the next example, we'll revisit the same search terms we used in the previous
# `Counts` analysis, and explore some of these settings.
#

###################################################################################################

# Set up some terms
terms = [['frontal lobe'], ['temporal lobe'], ['parietal lobe'], ['occipital lobe']]
words.add_terms(terms)

###################################################################################################
#
# EUtils Settings
# ~~~~~~~~~~~~~~~
#
# The Pubmed EUtils has several settings that can help control searches, including:
# - `field` : which part of the record to search for search results
# - `retmax` : the maximum number of records to return for a given search
# - `usehistory` : whether to temporarily store results remotely and use them for interim requests
#
# As some general guidelines, the `field` setting defaults to `TIAB` for titles and abstracts.
# The `retmax` should be set to some upper bound if your search terms are likely to
# return a large number of papers. The `usehistory` parameter should be set to True if
# you are running a large scrape, as this is more efficient.
#
# Word Collection Settings
# ~~~~~~~~~~~~~~~~~~~~~~~~
#
# If you are collecting data for a large number of search terms, that may return a large
# number of papers, then the `Words` collection can take a while, and the amount of
# data can become quite large.
#
# Because of this, the `Words` object offers a setting of how / when to save data:
# - `save_and_clear` : whether to save out collected data and clear per term
#
# Now, let's run our bigger collection, using some of these settings.
#

###################################################################################################

# Set up our database object, so we can save out data as we go
db = SCDB('lisc_db')

# Collect words data
words.run_collection(usehistory=True, retmax='15', save_and_clear=True, folder=db)

###################################################################################################
#
# Note that at this point, our Words object does not actually include the collected data,
# since we were saving and clearing the data out as we went.
#
# The Words object does still however have all the information about the Term data, and we
# can use that to help manage and reload our data, so it's worth saving as well.
#
# We will analyze our words data in the next tutorial, so for now lets save out the Words object.
#

###################################################################################################

save_object(words, 'tutorial_words', folder=db)
