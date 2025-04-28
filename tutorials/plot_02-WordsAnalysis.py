"""
Tutorial 02: Words Analysis
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
from lisc.io import SCDB, load_object

# Import plots that are available for words data
from lisc.plts.words import plot_wordcloud

###################################################################################################
# Articles Object
# ~~~~~~~~~~~~~~~
#
# LISC uses custom objects to store and organize collected words data.
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
# The :obj:`~.ArticlesAll` object aggregates collected data across all articles collected
# for a given search term.
#

###################################################################################################

# Collapse data across articles
arts_all = ArticlesAll(arts)

###################################################################################################
#
# It also has methods to create and check summaries created from the aggregate data.
#

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
# The `results` attribute contains a list of :class:`~.Articles` objects, one for each term.
#
# Note that the reloaded data is the raw data from the data collection.
#

###################################################################################################

# Reload the words object, specifying to also reload the article data
words = load_object('tutorial_words', directory=SCDB('lisc_db'), reload_results=True)

###################################################################################################
#
# The :meth:`~.Words.check_articles` method can be used to print out a summary of the articles
# that have been collected under each search term.
#

###################################################################################################

# Check the collected articles
words.check_articles()

###################################################################################################
# Processing Collected Data
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The :meth:`~.Words.process_articles` method can be used to do some preprocessing on the
# collected data.
#
# By default, the :func:`~.process_articles` function is used to process articles, which
# preprocesses journal and author names, and tokenizes the text data. You can also pass in
# a custom function to apply custom processing to the collected articles data.
#
# Note that some processing steps, like converting to the ArticlesAll representation,
# will automatically apply article preprocessing.
#

###################################################################################################

# Preprocess article data
words.process_articles()

###################################################################################################
#
# We can also aggregate data across articles, just as we did before, directly in the Words object.
#
# If you run the :meth:`~.Words.process_combined_results` method, then the
# `combined_results` attribute will contain the corresponding list of
# :class:`~.ArticlesAll` objects, also one for each term.
#

###################################################################################################

# Process collected data into aggregated data objects
words.process_combined_results()

###################################################################################################

# Plot a WordCloud of the collected data for the first term
plot_wordcloud(words.combined_results[0].words, 25)

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
# For example, this might include building profiles for each search term, based on
# data in collected articles. It might also include using methods from natural language
# processing, such as vector embeddings and/or similarity measures.
#
# Specific analyses might also be interested in exploring historical patterns in the literature,
# examining, for example, the history of when certain topics were written about, and in what
# journals, by which authors.
#
