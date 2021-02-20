"""Plots for words data."""

import numpy as np

from lisc.plts.utils import check_aliases, check_ax, savefig
from lisc.plts.wordcloud import create_wordcloud, conv_freqs
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')

###################################################################################################
###################################################################################################

@savefig
def plot_wordcloud(freq_dist, n_words, ax=None, **plt_kwargs):
    """Plot a wordcloud.

    Parameters
    ----------
    freq_dist : collections.Counter
        Frequency distribution of words to plot.
    n_words : int
        Number of top words to include in the wordcloud.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    plt_kwargs
        Additional keyword arguments for the plot.

    Examples
    --------
    See the :meth:`~.create_freq_dist` method of the :class:`~.ArticlesAll` object.
    """

    cloud = create_wordcloud(conv_freqs(freq_dist, n_words))

    ax = check_ax(ax, plt_kwargs.pop('figsize', (8, 8)))
    ax.imshow(cloud, **plt_kwargs)
    ax.axis("off")


@savefig
def plot_years(years, year_range=None, ax=None, **plt_kwargs):
    """Plot a histogram of the number publications across years.

    Parameters
    ----------
    years : collections.Counter
        Data on the number of publications per year.
    year_range : list of [int, int], optional
        The range of years to plot on the x-axis, inclusive.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    plt_kwargs
        Additional keyword arguments for the plot.

    Examples
    --------
    Plot a histogram of publication years:

    >>> from collections import Counter
    >>> plot_years(years=Counter({'2018': 25, '2019': 50, '2020':75}))

    Notes
    -----
    Publication years are collected together in the :class:`~.ArticlesAll` class.
    """

    ax = check_ax(ax, plt_kwargs.pop('figsize', (10, 5)))

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

    # Grab any plot inputs for labels
    fontsize = plt_kwargs.pop('fontsize', 18)

    # Add line and points to plot
    plt.plot(x_data, y_data,
             linewidth=check_aliases(plt_kwargs, ['linewidth', 'lw'], 3),
             marker=plt_kwargs.pop('marker', '.'),
             markersize=check_aliases(plt_kwargs, ['markersize', 'ms'], 10),
             markerfacecolor=plt_kwargs.pop('markerfacecolor', 'white'),
             **plt_kwargs)

    # Set plot limits
    plt.ylim([0, max(y_data) + int(0.03*(max(y_data) - min(y_data)))])

    # Add title & labels
    plt.xlabel('Year of Publication', fontsize=fontsize)
    plt.ylabel('Number of Articles', fontsize=fontsize)
