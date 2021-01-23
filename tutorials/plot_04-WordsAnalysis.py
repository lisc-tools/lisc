"""
Tutorial 04: Words Analysis
===========================

Analyzing collected text data and metadata.
"""

###################################################################################################
# Words Analyses
# --------------
#
# This tutorial covers exploring & analyzing words data.
#
# For this tutorial, we will reload and use the :class:`~.Words` object with
# the data that we collected in the last tutorial.
#
# Note that this tutorial requires some optional dependencies, including the
# `WordCloud <https://github.com/amueller/word_cloud>`_ module.
#

###################################################################################################

# Import the custom objects that are used to store collected words data
from lisc.data import Articles, ArticlesAll

# Import database and IO utilities to reload our previously collected data
from lisc.utils.db import SCDB
from lisc.utils.io import load_object

# Import plots that are available for words data
from lisc.plts.words import plot_wordcloud

# Import a helper function to install required nltk data
from lisc.utils.download import download_nltk_data

###################################################################################################
# NLTK Data
# ~~~~~~~~~
#
# This tutorial analyzes and tokenizes collected text which, if you are running locally,
# requires some data be available from NLTK. If you don't already have this data installed,
# you can run the :func:`~.download_nltk_data` function.
#

###################################################################################################
# Articles Object
# ~~~~~~~~~~~~~~~
#
# LISC uses a custom objects to store and organize collected words data.
#
# These objects are used internally in the :class:`~.Words` objects.
#
# If the data collection was set to save out data as it was collected, then
# :obj:`~.Articles` objects can be loaded individually, using the label
# of the search term.
#

###################################################################################################

# Set up database object
db = SCDB('lisc_db')

# Load raw data for a particular term
term = 'frontal lobe'
arts = Articles(term)
arts.load(db)

###################################################################################################
# ArticlesAll Object
# ~~~~~~~~~~~~~~~~~~
#
# There is also the :obj:`~.ArticlesAll` object, which is used to aggregate collected data
# across all articles collected for a given search term.
#
# The :obj:`~.ArticlesAll` object also has methods to create and check summaries
# created from the aggregate data.
#

###################################################################################################

# Collapse data across articles
arts_all = ArticlesAll(arts)

###################################################################################################

# Check an example summary
arts_all.create_summary()
arts_all.print_summary()

###################################################################################################
# Words Object
# ~~~~~~~~~~~~
#
# The :class:`~.Words` object can also be used to reload and analyze collected data.
#
# The `results` attribute of the :class:`~.Words` object, when loaded, contains a list of
# :class:`~.Articles` objects, one for each term.
#

###################################################################################################

# Reload the words object, specifying to reload the results
words = load_object('tutorial_words', directory=SCDB('lisc_db'), reload_results=True)

###################################################################################################

# Convert collected data into aggregated data objects
all_articles = [ArticlesAll(words[label]) for label in words.labels]

###################################################################################################

# Plot a WordCloud of the collected data for the first term
plot_wordcloud(all_articles[0].words, 25)

###################################################################################################
# Exploring Words Data
# --------------------
#
# The :class:`~.Words` object also has some methods for exploring the data, including
# allowing for indexing into and looping through collected results.
#

###################################################################################################

# Index results for a specific label
print(words['frontal lobe'])

###################################################################################################
#
# You can also loop through all the articles found for a specified search term.
#
# The iteration returns a dictionary with all the article data, which can be examined.
#

###################################################################################################

# Iterating through articles found for a search term of interest
for art in words['temporal lobe']:
    print(art['title'])

###################################################################################################
# Analyzing Words Data
# ~~~~~~~~~~~~~~~~~~~~
#
# Further analysis depends mostly on what one wants to do with the collected data.
#
# This might include, for example, building profiles for each search term, based on
# data in collected articles. It might also include using methods from natural language
# processing, such as vector embeddings and/or similarity measures.
#
# Specific analyses might also be interested in exploring historical patterns in the literature,
# examining, for example, the history of when certain topics were written about, and in what
# journals, by which authors.
#
