"""
Tutorial 04 - Words Analysis
============================
"""

###############################################################################
#
from lisc.core.db import SCDB
from lisc.data import Data
from lisc.data_all import DataAll

###############################################################################
# Data All
# --------

dd = DataAll(words.results[0])
dd.journal_counts

# Add data to path
db = SCDB()

# Load raw data from a particular ERP
term = 'autobiographical recall'
dat = Data(term)
dat.load(db)

# Collapse data across papers
all_dat = DataAll(dat)

###############################################################################
#
from lisc.plts.wc import make_wc

make_wc(all_dat.word_freqs, 25, term)
