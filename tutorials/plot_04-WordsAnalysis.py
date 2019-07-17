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

db = SCDB('lisc_db')

words = load_object('tutorial_words', folder=SCDB('lisc_db'))

###################################################################################################

# Reload all data
for ind in range(words.n_erps):
    words.results[ind].load()


###################################################################################################
#
# Data All
# --------
#

###################################################################################################

# Collect into list of aggragated data objects
all_dat = [DataAll(words[erp]) for erp in words.result_keys]


# Check an example summary
all_dat[0].create_summary()
all_dat[0].print_summary()

###################################################################################################



###################################################################################################


#dd = DataAll(words.results[0])
#dd.journal_counts

# Add data to path
#db = SCDB()

# Load raw data from a particular ERP
#term = 'autobiographical recall'
#dat = Data(term)
#dat.load(db)

# Collapse data across papers
#all_dat = DataAll(dat)

###################################################################################################

#
from lisc.plts.wordcloud import plot_wordcloud

plot_wordcloud(all_dat[0].word_freqs, 25)

###################################################################################################

# Exploring Words Data
# --------------------
#
# The words object also has a couple convenience methods for exploring the data.

# Indexing with labels
#print(words['brain'])

###################################################################################################

#
# Iterating through papers found from a particular search term
#  The iteration returns a dictionary with all the paper data
#for art in words['cognition']:
#    print(art['title'])
