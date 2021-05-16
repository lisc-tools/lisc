"""Utilities for data management and data object for LISC."""

from itertools import chain
from string import punctuation
from collections import Counter

from lisc.data.stopwords import STOPWORDS

###################################################################################################
###################################################################################################

def count_elements(lst, exclude=None):
    """Count how often each element occurs in a list.

    Parameters
    ----------
    lst : list
        List of items to count.
    exclude : list, optional
        Items to exclude from the frequency distribution.

    Returns
    -------
    counts : collections.Counter
        Counts for how often each item occurs in the input list.
    """

    counts = Counter(lst)

    # Drop the value for None
    try:
        counts.pop(None)
    except KeyError:
        pass

    # Drop any items set as exclusions
    if exclude:

        if isinstance(exclude[0], str):
            exclude = lower_list(exclude)

        for excl in exclude:
            try:
                counts.pop(excl)
            except KeyError:
                pass

    return counts


def threshold_counter(counter, value):
    """Threshold a Counter to only include elements above a certain count.

    Parameters
    ----------
    counter : Counter
        Counter object containing elements to threshold.
    value : int
        Value of the threshold to apply, inclusive.

    Returns
    -------
    Counter
        Counter object with only values above a threshold.
    """

    return Counter({key: val for key, val in counter.items() if val >= value})


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


def combine_lists(lst):
    """Combine list of lists into one large list.

    Parameters
    ----------
    lst : list of list
        Embedded lists to combine.

    Returns
    -------
    out : list
        Combined (flat) list.
    """

    return list(chain.from_iterable(drop_none(lst)))


def tokenize(text):
    """Tokenize a string of text into individual words.

    Parameters
    ----------
    text : str
        Text to tokenize.

    Returns
    -------
    list of str
        Tokenized text.
    """

    punc_keep = ['-', '/']
    punc_custom = ['.', ',']

    # Drop general punctuation from the string
    for punc in set(punctuation) - set(punc_keep + punc_custom):
        text = text.replace(punc, '')

    # For some custom punctuation, replace them with a space
    for custom_punc in set([el + ' ' for el in punc_custom]):
        text = text.replace(custom_punc, ' ')

    # The final period may be missed, so check and remove if so
    if len(text) > 0 and text[-1] == '.':
        text = text[:-1]

    return text.split()


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

    # Converting to use a dictionary makes checking a little more efficient
    stopwords = Counter(stopwords)

    # Tokenize and remove stopwords
    words_cleaned = [word.lower() for word in tokenize(text) if word.lower() not in stopwords]

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
