"""
Tutorial 04 - Words Analysis
============================

Analyzing scraped words data.
"""

###################################################################################################
#
# Words Analyses
# --------------
#
# This tutorial explores the built in utilities for exploring & anayzing words data.
#

###################################################################################################

from lisc.core.db import SCDB
from lisc.data import Data, DataAll

###################################################################################################
#
# Data All
# --------

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
#from lisc.plts.wc import make_wc

#make_wc(all_dat.word_freqs, 25, term)

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
