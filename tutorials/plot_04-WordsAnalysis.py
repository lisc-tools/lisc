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
# This tutorial covers exploring & anayzing words data.
#
# For this tutorial, we will reload and use the `Words` data that we collected
# in the last tutorial.
#

###################################################################################################

from lisc import SCDB, load_object
from lisc.data import Data, DataAll

from lisc.plts.wordcloud import plot_wordcloud

###################################################################################################
#
# Data Objects
# ~~~~~~~~~~~~
#
# LISC uses a custom object to store and organize collected words data.
#
# These objects are used internally in the `Words` objects.
#
# If th data collection was set to save out data as it was collected, then these Data
# objects can be loaded individually, using the label of the search term.
#

###################################################################################################

# Set up database object
db = SCDB('lisc_db')

# Load raw data for a particular term
term = 'frontal lobe'
data = Data(term)
data.load(db)

###################################################################################################
#
# DataAll Object
# ~~~~~~~~~~~~~~
#
# There is also the `DataAll` object, which is variant which can be used to
# aggregate collected data across all articles collected for a given search term.
#
# The DataAll also have methods to create and check summaries created from the aggregate data.
#

###################################################################################################

# Collapse data across papers
data_all = DataAll(data)

###################################################################################################

# Check an example summary
data_all.create_summary()
data_all.print_summary()

###################################################################################################
#
# Words Object
# ~~~~~~~~~~~~
#
# The `Words` object can also be used to reload and analyze collected data.
#
# The `results` attribute of the `Words` object, when loaded, contains a list of
# Data objects, one for each term.
#

###################################################################################################

# Reload the words object
words = load_object('tutorial_words', folder=SCDB('lisc_db'))

###################################################################################################

# Reload all data
for ind in range(words.n_terms):
    words.results[ind].load(folder=db)

###################################################################################################

# Collect into list of aggragated data objects
all_dat = [DataAll(words[label]) for label in words.labels]

###################################################################################################

# Plot a WordCloud of the collected data for the first term
plot_wordcloud(all_dat[0].words, 25)

###################################################################################################
#
# Exploring Words Data
# --------------------
#
# The words object also has a couple convenience methods for exploring the data.
#

###################################################################################################

# Indexing with labels
print(words['frontal lobe'])

###################################################################################################

# Iterating through papers found from a particular search term
#  The iteration returns a dictionary with all the paper data
for art in words['temporal lobe']:
    print(art['title'])
