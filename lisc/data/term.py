"""Term object for LISC."""

from collections import namedtuple

###################################################################################################
###################################################################################################

class Term(namedtuple('Term', ['label', 'search', 'inclusions', 'exclusions'])):
    """Search term definition with inclusion & exclusion words.

    Parameters
    ----------
    label : str
        Label for the term.
    search : list of str
        Search terms.
    inclusions : list of str
        Inclusion words for search terms.
    exclusions : list of str
        Exclusion words for search terms.

    Examples
    --------
    Define a search term, with inclusions and exclusions:

    >>> Term('brain', ['frontal lobe', 'temporal lobe'], ['EEG'], ['MRI'])
    Term(label='brain', search=['frontal lobe', 'temporal lobe'], inclusions=['EEG'], exclusions=['MRI'])
    """
    __slots__ = ()
