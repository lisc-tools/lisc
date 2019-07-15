"""LISC plots - plots for single terms."""

from lisc.plts.utils import check_ax, savefig
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')

###################################################################################################
###################################################################################################

@savefig
def plot_years(year_counts, year_range=None, ax=None):
    """Plot publications across years histogram.

    Parameters
    ----------
    year_counts : list of tuple of (int, int)
        Data on the number of publications per year.
    year_range : list of [int, int], optional
        The range of years to plot on the x-axis.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    """

    ax = check_ax(ax, (10, 5))

    # Extract x & y data to plot
    x_dat = [xd[0] for xd in year_counts]
    y_dat = [yd[1] for yd in year_counts]

    # Add line and points to plot
    plt.plot(x_dat, y_dat)
    plt.plot(x_dat, y_dat, '.', markersize=16)

    # Set plot limits
    if year_range:
        plt.xlim([year_range[0], year_range[1]])
    plt.ylim([0, max(y_dat)+5])

    # Add title & labels
    plt.title('Publication History', fontsize=24, fontweight='bold')
    plt.xlabel('Year', fontsize=18)
    plt.ylabel('# Pubs', fontsize=18)
