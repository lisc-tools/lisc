"""
Tutorial 03: Words Collection
=============================

Collecting literature data, including text and metadata for specified search terms.
"""

###################################################################################################
# Words Analysis
# --------------
#
# Another way to analyze the literature is to collect text and meta-data from
# all articles found for requested search terms.
#

###################################################################################################

# Import the Words object, which is used for words collection
from lisc import Words

# Import the SCDB object, which organizes a database structure for saved data
from lisc.utils.db import SCDB

# Import a utility function for saving out collected data
from lisc.utils.io import save_object

###################################################################################################
# Words Object
# ------------
#
# The :class:`~.Words` object is used to collect and analyze text data and article metadata.
#
# Search terms are specified, as previously introduced, to find articles of interest,
# from which text data and meta-data is collected.
#

###################################################################################################

# Set some search terms
terms = [['brain'], ['body']]

###################################################################################################

# Initialize Words object and set the terms to search for
words = Words()
words.add_terms(terms)

###################################################################################################
#
# To get started, we will first run a collection of words data, collecting up to
# 5 articles for each search term, as specified by the `retmax` parameter.
#

###################################################################################################

# Collect words data
words.run_collection(retmax='5')

###################################################################################################
# LISC Data Objects
# ~~~~~~~~~~~~~~~~~
#
# LISC uses custom objects to store collected words data.
#
# The :obj:`~.Articles` object stores data for each collected article.
#
# Collected data includes:
#
# - titles
# - journals
# - authors
# - publication years
# - abstract text
# - keywords
# - DOIs
#

###################################################################################################

# Check the collected words data
print(words.results)

###################################################################################################

# Check some specific fields of the collected data
print(words.results[0].n_articles)
print(words.results[0].titles)

###################################################################################################
# Word Collections
# ----------------
#
# Collected words data from articles can become quite large. We will often want to use
# some of the available EUtils settings to help control what is collected, and how the data
# collection proceeds.
#
# In the next example, we'll revisit the same search terms we used in the previous
# co-occurence analysis, and explore some of these settings.
#

###################################################################################################

# Set search terms of interest
terms = [['frontal lobe'], ['temporal lobe'], ['parietal lobe'], ['occipital lobe']]
words.add_terms(terms)

###################################################################################################
# EUtils Settings
# ~~~~~~~~~~~~~~~
#
# The Pubmed EUtils has several settings that can help control searches, including:
#
# - `field` : which part of the record to search for search results
# - `retmax` : the maximum number of records to return for a given search
# - `usehistory` : whether to temporarily store results remotely and use them for interim requests
#
# For some general guidelines:
#
# - the `field` setting defaults to `TIAB` for titles and abstracts
# - the `retmax` should be set to an upper bound for the number of articles you would like
#   to collect, especially if your search terms are likely to return a large number of articles
# - the `usehistory` parameter should be set to True if you are running a large collection,
#   as this is more efficient
#
# Word Collection Settings
# ~~~~~~~~~~~~~~~~~~~~~~~~
#
# For larger collections, the collectio my take a while and return a large amount of data.
#
# Because of this, the :class:`~.Words` object allows for continuously saving collected data.
# If set to True, the `save_and_clear` parameter saves out collected data, and clears the
# object per term, so that collected data does not have to stay in RAM.
#
# Now, let's run our bigger collection, using some of these settings.
#

###################################################################################################

# Set up our database object, so we can save out data as we go
db = SCDB('lisc_db')

# Collect words data
words.run_collection(usehistory=True, retmax='15', save_and_clear=True, directory=db)

###################################################################################################
#
# After this collection, the Words object does not actually include the collected data,
# as the data was saved and cleared throughout the collection.
#
# The Words object does still have all the information about the search terms, which we can
# use to reload our data, so it is still worth saving as well.
#
# We will analyze our words data in the next tutorial. For now lets save out the Words object.
#

###################################################################################################

# Save out the words data
save_object(words, 'tutorial_words', directory=db)
