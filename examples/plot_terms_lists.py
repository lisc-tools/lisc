"""
Database and Terms Lists
========================

Organizing lists of terms to be used for LISC analyses.
"""

###################################################################################################

from lisc.core.db import SCDB, create_file_structure

###################################################################################################

# Create a database file structure.
#   Note that when called without a path argument input,
#   the folder structure is made in the current directory.
db = create_file_structure()

###################################################################################################

# Check the file structure for the created database
db.check_file_structure()

###################################################################################################
#
# TODO: MORE WORDS HERE
#
