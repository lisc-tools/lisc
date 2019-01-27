"""
Tutorial 00 - Overview
======================
"""

###############################################################################
# LISC
# ----
#
# LIterature SCanner (LISC) is a python module for scraping literature data. It is basically a wrapper around the Pubmed [E-Utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/).
#
# LISC provides for two different 'types' of scraping, 'Counts' and 'Words'.

###############################################################################
# Counts
# ------
#
# 'Counts' scrapes for co-occurence of given set(s) of terms.
#

###############################################################################
# Words
# -----
#
# 'Words' scrapes abstract text data, and paper meta-data, for all papers found for a given set of terms.
#

###############################################################################
# Functions vs. Objects
# ---------------------
#
# Each of these types of scrapes can be called in one of two ways, either by using scrape functions provided by LISC (function approach), or by using objects provided by LISC (OOP approach).
#
# Note that, under the hood, these methods are the same, the OOP oriented approach simply provides wrappers around the scraping functions.
