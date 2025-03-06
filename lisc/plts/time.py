"""Plots for data across time."""

from lisc.analysis.time import get_counts_across_years
from lisc.plts.utils import check_ax, savefig
from lisc.modutils.dependencies import safe_import

plt = safe_import('.pyplot', 'matplotlib')

###################################################################################################
###################################################################################################

@savefig
def plot_results_across_years(results, ax=None, **plt_kwargs):
    """Plot counts data from across years.

    Parameters
    ----------
    results : dict
        Results collected across time.
        Each key should reflect the start year, and each value is a object with search results.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    plt_kwargs
        Additional keyword arguments for the plot.
    """

    labels, years, data = get_counts_across_years(results)

    ax = check_ax(ax, plt_kwargs.pop('figsize', (6, 3.5)))

    fontsize = plt_kwargs.pop('fontsize', 18)
    xlabel = plt_kwargs.pop('xlabel', 'Year of Publication')
    ylabel = plt_kwargs.pop('ylabel', 'Number of Articles')
    legend_fontsize = plt_kwargs.pop('legend_fontsize', 12)
    xlim = plt_kwargs.pop('xlim', None)
    ylim = plt_kwargs.pop('ylim', None)

    for label, counts in zip(labels, data):
        plt.plot(years, counts, alpha=0.85, label=label, **plt_kwargs)

    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set(xlim=xlim, ylim=ylim)

    plt.legend(fontsize=legend_fontsize)
