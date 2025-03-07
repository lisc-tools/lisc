"""
Tutorial 07: MetaData
=====================

Exploring metadata collected and saved during data collections.
"""

from lisc.io import SCDB, load_object

###################################################################################################
# Metadata
# --------
#
# Whenever you collect data with LISC, meta data is collected about the API requests
# and databases accessed.
#
# Here we will explore the metadata collected during our previous investigations.
#

###################################################################################################

# Reload the counts object
counts = load_object('tutorial_counts', SCDB('lisc_db'))

###################################################################################################
# Metadata Object
# ---------------
#
# Metadata information is collected into a custom :class:`~.MetaData` object.
#
# If you are collecting data using the LISC object, such as the :class:`~.Counts`
# or :class:`~.Words` object, this collection information is attached and saved
# to the object as the `meta_data` attribute.
#

###################################################################################################

# Check the date on which the collection happened
print(counts.meta_data.date)

###################################################################################################

# Check the information about the database from which data was collected
counts.meta_data.db_info

###################################################################################################
#
# For the next part, we'll reload the :class:`~.Words` object, which also has stored meta data.
#

###################################################################################################

# Reload the words object
words = load_object('tutorial_words', SCDB('lisc_db'))

###################################################################################################
# Requester MetaData
# ~~~~~~~~~~~~~~~~~~
#
# The collected metadata also includes information from the :class:`~.Requester`
# object, which is used to launch URL requests.
#
# The Requester object tracks information including when URL requests were
# launched and the number of requests made.
#

###################################################################################################

# Check meta data from the requester object
words.meta_data.requester
