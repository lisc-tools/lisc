"""Utilities for data management and data object for LISC."""

from collections import Counter

from nltk import word_tokenize
from nltk.corpus import stopwords

###################################################################################################
###################################################################################################

STOPWORDS = stopwords.words('english')

def count_elements(data_lst):
    """Count how often each element occurs in a list.

    Parameters
    ----------
    data_lst : list
        List of items to count.

    Returns
    -------
    counts : collections.Counter
        Counts for how often each item occurs in the input list.
    """

    counts = Counter(data_lst)

    try:
        counts.pop(None)
    except KeyError:
        pass

    return counts


def drop_none(lst):
    """Creates a generator that return elements of an iterable, dropping None values.

    Parameters
    ----------
    lst : list
        Input iterable.

    Yields
    ------
    el
        Elements of the input list. Can be of any type, except None.
    """

    for el in lst:
        if el is not None:
            yield el


def combine_lists(in_lst):
    """Combine list of lists into one large list.

    Parameters
    ----------
    in_lst : list of list of str
        Embedded lists to combine.

    Returns
    -------
    out : list of str
        Combined list.

    Notes
    -----
    This function also converts all contained strings to lowercase.
    """

    out = []

    for el in in_lst:
        if el:
            out.extend(lower_list(el))

    return out


def convert_string(text, stopwords=STOPWORDS):
    """Convert strings of text into tokenized lists of words.

    Parameters
    ----------
    text : str
        Text as one long string.
    stopwords : list of str
        Stopwords to remove from the text.

    Returns
    -------
    words_cleaned : list of str
        List of tokenized words, after processing.

    Notes
    -----
    This function sets text to lower case, and removes stopwords and punctuation.
    """

    words = word_tokenize(text)
    words_cleaned = [word.lower() for word in words if (
        (not word.lower() in stopwords) & word.isalnum())]

    return words_cleaned


def lower_list(lst):
    """Convert a list of strings to all be lowercase.

    Parameters
    ----------
    lst : list of str
        List of string to convert to lowercase.

    Returns
    -------
    lst of str
        List of string with all lowercase.
    """

    return [el.lower() for el in lst]
