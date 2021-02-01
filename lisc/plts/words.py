"""Plots for words data."""

import numpy as np

from lisc.plts.utils import check_ax, savefig
from lisc.plts.wordcloud import create_wordcloud, conv_freqs
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')

###################################################################################################
###################################################################################################

@savefig
def plot_wordcloud(freq_dist, n_words, ax=None):
    """Plot a wordcloud.

    Parameters
    ----------
    freq_dist : collections.Counter
        Frequency distribution of words to plot.
    n_words : int
        Number of top words to include in the wordcloud.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.

    Examples
    --------
    See the :meth:`~.create_freq_dist` method of the :class:`~.ArticlesAll` object.
    """

    cloud = create_wordcloud(conv_freqs(freq_dist, n_words))

    ax = check_ax(ax, (8, 8))
    ax.imshow(cloud)
    ax.axis("off")


@savefig
def plot_years(years, year_range=None, ax=None):
    """Plot a histogram of the number publications across years.

    Parameters
    ----------
    years : collections.Counter
        Data on the number of publications per year.
    year_range : list of [int, int], optional
        The range of years to plot on the x-axis, inclusive.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.

    Examples
    --------
    Plot a histogram of publication years:

    >>> from collections import Counter
    >>> plot_years(years=Counter({'2018': 25, '2019': 50, '2020':75}))

    Notes
    -----
    Publication years are collected together in the :class:`~.ArticlesAll` class.
    """

    ax = check_ax(ax, (10, 5))

    # Get the plot data, making sure it is sorted
    sort_inds = np.argsort(list(years.keys()))
    x_data = np.array(list(years.keys()))[sort_inds]
    y_data = np.array(list(years.values()))[sort_inds]

    # Restrict the data to the desired plot range
    if year_range:
        range_inds = np.logical_and(x_data >= (year_range[0] if year_range[0] else -np.inf),
                                    x_data <= (year_range[1] if year_range[1] else np.inf))
        x_data = x_data[range_inds]
        y_data = y_data[range_inds]

    # Add line and points to plot
    plt.plot(x_data, y_data)
    plt.plot(x_data, y_data, '.', markersize=16)

    # Set plot limits
    plt.ylim([0, max(y_data)+3])

    # Add title & labels
    plt.title('Publication History', fontsize=24, fontweight='bold')
    plt.xlabel('Year of Publication', fontsize=18)
    plt.ylabel('Number of Articles', fontsize=18)
