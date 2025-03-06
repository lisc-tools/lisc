"""Word cloud plots."""

import random

from lisc.modutils.dependencies import safe_import

wc = safe_import('wordcloud')

###################################################################################################
###################################################################################################

def create_wordcloud(words):
    """Create WordCloud object.

    Parameters
    ----------
    words : dict
        Words for the wordcloud, with their corresponding frequencies.

    Returns
    -------
    wc : WordCloud
        Wordcloud object.
    """

    cloud = wc.WordCloud(background_color=None,
                         mode='RGBA',
                         width=800,
                         height=400,
                         prefer_horizontal=1,
                         relative_scaling=0.5,
                         min_font_size=25,
                         max_font_size=80).generate_from_frequencies(words)

    cloud.recolor(color_func=_grey_color_func, random_state=3)

    return cloud


def conv_freqs(freq_dist, n_words):
    """Convert a Counter object into a dictionary.

    Parameters
    ----------
    freq_dist : collections.Counter
        Frequency distribution of words.
    n_words : int
        Number of words to extract.

    Returns
    -------
    dict
        Words with their corresponding frequencies.
    """

    return dict(freq_dist.most_common(n_words))


def _grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """Function for custom coloring with a gray pallet.
    From here: https://amueller.github.io/word_cloud/auto_examples/a_new_hope.html
    """

    return "hsl(0, 0%%, %d%%)" % random.randint(25, 50)
