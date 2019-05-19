"""LISC plots - word clouds."""

import os
import random

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from lisc.core.db import check_db
from lisc.plts.utils import _save_fig

###################################################################################################
###################################################################################################

def make_wc(freq_dist, n_words, label, save_fig=False):
    """Create and display wordcloud.

    Parameters
    ----------
    freq_dist : xx
        xx
    n_words : int
        Number of top words to include in the wordcloud.
    label : xx
        xx
    save_fig : boolean
        Whether to save out the wordcloud.
    """

    wc = create_wc(conv_freqs(freq_dist, 20))

    plt.figure(figsize=(10, 10))
    plt.imshow(wc)
    plt.axis("off")

    _save_fig(save_fig, label)


def conv_freqs(freq_dist, n_words):
    """Convert FreqDist into a list of tuple for creating a WordCloud.

    Parameters
    ----------
    freq_dist : nltk FreqDist() object
        Frequency distribution of words from text.
    n_words : int
        Number of words to extract for plotting.

    Returns
    -------
    dict
        All words with their corresponding frequecies.
    """

    return dict(freq_dist.most_common(n_words))


def create_wc(words_in):
    """Create WordCloud object.

    Parameters
    ----------
    words_in : list of tuple
        Words to plot, with their corresponding frequencies.

    Returns
    -------
    wc : WordCloud() object
        Wordcloud definition.
    """

    # Create the WordCloud object
    wc = WordCloud(background_color=None,
                   mode='RGBA',
                   width=800,
                   height=400,
                   prefer_horizontal=1,
                   relative_scaling=0.5,
                   min_font_size=25,
                   max_font_size=80).generate_from_frequencies(words_in)

    # Change colour scheme to grey
    wc.recolor(color_func=_grey_color_func, random_state=3)

    return wc

############################################################################################
############################################################################################

def _grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """Function for custom coloring - use gray pallete.
    From here: https://amueller.github.io/word_cloud/auto_examples/a_new_hope.html
    """

    return "hsl(0, 0%%, %d%%)" % random.randint(25, 50)
