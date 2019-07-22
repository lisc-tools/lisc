"""
Tutorial 04 - Words Analysis
============================

Analyzing collected text data and metadata.
"""

###################################################################################################
#
# Words Analyses
# --------------
#
# This tutorial explores the built in utilities for exploring & anayzing words data.
#

###################################################################################################

from lisc import SCDB, load_object
from lisc.data import Data, DataAll

###################################################################################################

# Set up database object
db = SCDB('lisc_db')

###################################################################################################

# Load raw data from a particular term
term = 'frontal lobe'
data = Data(term)
data.load(db)

###################################################################################################

# Collapse data across papers
all_data = DataAll(data)

###################################################################################################


# Reload the words object
words = load_object('tutorial_words', folder=SCDB('lisc_db'))

###################################################################################################

# Reload all data
for ind in range(words.n_terms):
    words.results[ind].load(folder=db)

###################################################################################################
#
# Data All
# --------
#

###################################################################################################

# Collect into list of aggragated data objects
all_dat = [DataAll(words[label]) for label in words.labels]


# Check an example summary
all_dat[0].create_summary()
all_dat[0].print_summary()

###################################################################################################

example_alldat = DataAll(words.results[0])
example_alldat.journal_counts

###################################################################################################

#
from lisc.plts.wordcloud import plot_wordcloud

plot_wordcloud(all_dat[0].word_freqs, 25)

###################################################################################################
#
# Exploring Words Data
# --------------------
#
# The words object also has a couple convenience methods for exploring the data.

###################################################################################################

# Indexing with labels
print(words['frontal lobe'])

###################################################################################################

# Iterating through papers found from a particular search term
#  The iteration returns a dictionary with all the paper data
for art in words['temporal lobe']:
    print(art['title'])
