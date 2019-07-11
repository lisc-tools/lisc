"""LISC plots - plots for group analysis."""

from lisc.plts.utils import check_ax, savefig, get_cmap
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')
sns = safe_import('seaborn')
hier = safe_import('.cluster.hierarchy', 'scipy')

###################################################################################################
###################################################################################################

@savefig
def plot_matrix(dat, x_labels=None, y_labels=None, square=False, ax=None):
    """Plot the matrix of percent asscociations between terms.

    Parameters
    ----------
    dat : 2d array
        Data to plot, as a matrix.
    x_labels : list of str
        Labels for the x-axis.
    y_labels : list of str
        Labels for the y-axis.
    square : bool
        Whether to plot each cell as equal sized squares.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    """

    sns.heatmap(dat, square=square, xticklabels=x_labels, yticklabels=y_labels,
                ax=check_ax(ax, (10, 12)))


@savefig
def plot_clustermap(dat, cmap='purple', ax=None):
    """Plot clustermap.

    Parameters
    ----------
    dat : 2d array
        Data to plot, as a clustermap.
    cmap : matplotlib.cmap
        Colormap to use for the plot.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    """

    # Set up plotting and aesthetics
    sns.set()
    sns.set_context("paper", font_scale=1.5)

    ax = check_ax(ax, (12, 10))

    if isinstance(cmap, str):
        cmap = get_cmap(cmap)

    cg = sns.clustermap(dat, cmap=cmap, method='complete', metric='cosine')

    # Fix axes
    cg.cax.set_visible(True)
    _ = plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=60, ha='right')
    _ = plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)


@savefig
def plot_dendrogram(dat, labels, ax=None):
    """Plot dendrogram.

    Parameters
    ----------
    dat : 2d array
        Data to plot, as a dendrogram.
    labels : list of str
        Labels for the dendrogram.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    """

    linkage_data = hier.linkage(dat, method='complete', metric='cosine')

    dendro_plot = hier.dendrogram(linkage_data, orientation='left', labels=labels,
                                  color_threshold=0.25, leaf_font_size=12,
                                  ax=check_ax(ax, (3, 15)))
