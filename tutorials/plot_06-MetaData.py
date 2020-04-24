"""
Tutorial 06: MetaData
=====================

Exploring the meta data saved during data collections.
"""

from lisc.utils.db import SCDB
from lisc.utils.io import load_object

###################################################################################################
# Metadata
# --------
#
# Whenever you collect data with LISC, some meta data is collected about the
# API requests and databases accessed.
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
# Meta data information is collected into a custom :class:`~.MetaData` object.
#
# If you are collecting data using the LISC object, such as the :class:`~.Counts`
# or :class:`~.Words` object, this collection information is attached and saved
# to the object, as the `meta_data` attribute.
#

###################################################################################################

# Check the date on which the collection happened
print(counts.meta_data.date)

###################################################################################################

# Check the information about the database from which data was collected
counts.meta_data.db_info

###################################################################################################
#
# For the next part, we'll reload the :class:`~.Words` object, which has the same meta data
# object available.
#

###################################################################################################

# Reload the words object
words = load_object('tutorial_words', SCDB('lisc_db'))

###################################################################################################
# Requester MetaData
# ~~~~~~~~~~~~~~~~~~
#
# The collected meta data also includes information from the :class:`~.Requester`
# object, which is used to launch URL requests.
#
# The Requester object tracks information including when URL requests were
# launched and the number of requests made.
#

###################################################################################################

# Check meta data from the requester object
words.meta_data.requester

###################################################################################################
# The End!
# ~~~~~~~~
#
# That is the end of the main tutorial for LISC!
#
# There are some additional stand alone examples on the
# `examples <https://lisc-tools.github.io/lisc/auto_tutorials/index.html>`_
# page.
#
# If you have any further questions, or find any problems with the code,
# please get in touch through the Github
# `issues <https://github.com/lisc-tools/lisc/issues>`_
# page.
#
