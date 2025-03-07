"""
Tutorial 03: 1D Counts
======================

Collect term occurrence data from the scientific literature.
"""

###################################################################################################
# Term Occurrence
# ---------------
#
# One thing we may want to examine in the literature is how common certain research topics are.
#
# To do so, we can search for term occurrence - how often particular search terms occur in the
# the literature. This will be the topic of the current tutorial.
#

###################################################################################################

# Import the Counts1D object, which is used for co-occurrence analysis
from lisc import Counts1D

###################################################################################################
# Counts1D Object
# ---------------
#
# The :class:`~.Counts1D` object is used to handle term occurrence collection and analyses.
#
# This object is based on the :class:`~.Base` object introduced in the prior tutorial,
# meaning we can define and add terms to it like introduced there.
#

###################################################################################################

# Set up some terms to search for
terms = [['frontal lobe'], ['temporal lobe'], ['parietal lobe'], ['occipital lobe']]

###################################################################################################

# Initialize counts object & add the terms that we want to collect co-occurrences for
counts1d = Counts1D()
counts1d.add_terms(terms)

###################################################################################################
#
# As before, we can check the terms that we've added to the object.
#
# Note that adding terms could also include adding synonyms, inclusion, and exclusion terms
# (see previous tutorials).
#

###################################################################################################

# Check terms definition
counts1d.check_terms()

###################################################################################################
#
# Now we are ready to run collection!
#

###################################################################################################

# Collect term occurrence data
counts1d.run_collection(verbose=True)

###################################################################################################
#
# We have now collected some literature data!
#
# The :class:`~.Counts1D` object will now contain data on term occurrence in the literature.
#
# This is stored in the `counts` attribute of the object.
#
# We can check the results of the occurrence search with the `check_counts` method.
#

###################################################################################################

# Check counts per term
counts1d.check_counts()

###################################################################################################
#
# If we want to compare term occurrences, we can also use the `check_top` method to check
# the term with the most occurrences.
#

###################################################################################################

# Check top term
counts1d.check_top()

###################################################################################################
#
# By itself, term occurrence provides some insight into the literature, in a simple way.
#
# In the next tutorial we will build up from this simple term occurrence to examine term
# co-occurrence, allowing for examining more complex questions about how different research
# topics relate to each other.
#
