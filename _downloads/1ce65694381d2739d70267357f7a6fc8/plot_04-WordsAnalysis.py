"""
Tutorial 04: Words Analysis
===========================

Analyzing collected text data and metadata.
"""

###################################################################################################
#
# Words Analyses
# --------------
#
# This tutorial covers exploring & analyzing words data.
#
# For this tutorial, we will reload and use the `Words` data that we collected
# in the last tutorial.
#

###################################################################################################

from lisc.data import Articles, ArticlesAll
from lisc.utils.db import SCDB
from lisc.utils.io import load_object

from lisc.plts.words import plot_wordcloud

###################################################################################################
#
# Articles Object
# ~~~~~~~~~~~~~~~
#
# LISC uses a custom objects to store and organize collected words data.
#
# These objects are used internally in the `Words` objects.
#
# If the data collection was set to save out data as it was collected, then 'Articles'
# objects can be loaded individually, using the label of the search term.
#

###################################################################################################

# Set up database object
db = SCDB('lisc_db')

# Load raw data for a particular term
term = 'frontal lobe'
arts = Articles(term)
arts.load(db)

###################################################################################################
#
# ArticlesAll Object
# ~~~~~~~~~~~~~~~~~~
#
# There is also the `ArticlesAll` object, which is variant which can be used to
# aggregate collected data across all articles collected for a given search term.
#
# The ArticlesAll object also has methods to create and check summaries
# created from the aggregate data, across all articles for a given search term.
#

###################################################################################################

# Collapse data across articles
arts_all = ArticlesAll(arts)

###################################################################################################

# Check an example summary
arts_all.create_summary()
arts_all.print_summary()

###################################################################################################
#
# Words Object
# ~~~~~~~~~~~~
#
# The `Words` object can also be used to reload and analyze collected data.
#
# The `results` attribute of the `Words` object, when loaded, contains a list of
# Articles objects, one for each term.
#

###################################################################################################

# Reload the words object
words = load_object('tutorial_words', directory=SCDB('lisc_db'))

###################################################################################################

# Reload all data
for ind in range(words.n_terms):
    words.results[ind].load(directory=db)

###################################################################################################

# Collect into list of aggragated data objects
all_articles = [ArticlesAll(words[label]) for label in words.labels]

###################################################################################################

# Plot a WordCloud of the collected data for the first term
plot_wordcloud(all_articles[0].words, 25)

###################################################################################################
#
# Exploring Words Data
# --------------------
#
# The Words object also has some methods for exploring the data.
#

###################################################################################################

# Indexing with labels
print(words['frontal lobe'])

###################################################################################################

# Iterating through articles found from a particular search term
#  The iteration returns a dictionary with all the article data
for art in words['temporal lobe']:
    print(art['title'])

###################################################################################################
#
# Analyzing Words Data
# ~~~~~~~~~~~~~~~~~~~~
#
# Further analysis is mostly determined by what one wants to do with the collected data.
#
# Words data can be used to, for example, build profiles for search terms, based
# on distributions of words in related articles. This could include methods from
# natural language processing such as vector embeddings, measuring similarities and
# differences between terms.
#
# Other analyses could explore historical patterns in the literature exploring, for
# exploring the history of when certain topics were written about, and in what
# journals, by which authors.
#