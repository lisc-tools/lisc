"""LISC plots - word clouds."""

import random

from lisc.core.modutils import safe_import
from lisc.plts.utils import savefig, check_ax

wc = safe_import('wordcloud')

###################################################################################################
###################################################################################################

def create_wordcloud(words):
    """Create WordCloud object.

    Parameters
    ----------
    words : dict
        Words to plot, with their corresponding frequencies.

    Returns
    -------
    wc : WordCloud() object
        Wordcloud definition.
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
    """Convert FreqDist into a dictionary for creating a WordCloud.

    Parameters
    ----------
    freq_dist : nltk FreqDist() object
        Frequency distribution of words from text.
    n_words : int
        Number of words to extract for plotting.

    Returns
    -------
    dict
        All words with their corresponding frequencies.
    """

    return dict(freq_dist.most_common(n_words))


def _grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """Function for custom coloring - use gray pallete.
    From here: https://amueller.github.io/word_cloud/auto_examples/a_new_hope.html
    """

    return "hsl(0, 0%%, %d%%)" % random.randint(25, 50)
