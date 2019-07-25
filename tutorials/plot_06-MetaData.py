"""
Tutorial 06: MetaData
=====================

Exploring the meta data saved during data collections.
"""

from lisc import SCDB, load_object

###################################################################################################
#
# Metadata
# --------
#
# Whenever you collect data with LISC, there is some meta data on the
# API requests and databases collected.
#

###################################################################################################

# Reload the counts object
counts = load_object('tutorial_counts', SCDB('lisc_db'))

###################################################################################################
#
# Metadata Object
# ---------------
#
# This collection information is collected into a custom MetaData object,
#
# If you are collecting data using the LISC object, such as the `Counts` or `Words`
# object, this collection information is attached and saved to the object, as the
# `meta_data` attribute.
#

###################################################################################################

# Check the date on which the collection happened
print(counts.meta_data.date)

###################################################################################################

# Check the information about the database from which data was collected
counts.meta_data.db_info

###################################################################################################
#
# For the next part, we'll reload the `Words` object, which has the same meta data
# object available.
#

###################################################################################################

# Reload the words object
words = load_object('tutorial_words', SCDB('lisc_db'))

###################################################################################################
#
# Requester MetaData
# ~~~~~~~~~~~~~~~~~~
#
# The collected meta data also includes information from the Requester object,
# which is used to launch URL requests
#
# The Requester object track information including when URL requests were
# launched and the number of requests that were made.
#

###################################################################################################

# Check meta data from the requester object
words.meta_data.requester

###################################################################################################
#
# The End!
# ~~~~~~~~
#
# That is the end of the main tutorial for LISC!
#
# There are some additional stand alone examples on the
# `examples <https://lisc-tools.github.io/lisc/auto_tutorial/index.html>`_
# page.
#
# If you have any further questions, or find any problems with the code,
# pleas get in touch through the Github
# `issues <https://github.com/lisc-tools/lisc/issues>`_
# page.
#
