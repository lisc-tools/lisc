"""LISC plots - plots for group analysis."""

from lisc.plts.utils import check_args, check_ax, savefig, get_cmap
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')
sns = safe_import('seaborn')
hier = safe_import('.cluster.hierarchy', 'scipy')

###################################################################################################
###################################################################################################

@savefig
def plot_matrix(data, x_labels=None, y_labels=None, square=False, ax=None):
    """Plot the matrix of percent asscociations between terms.

    Parameters
    ----------
    data : 2d array
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

    sns.heatmap(data, square=square, ax=check_ax(ax, (8, 8)),
                **check_args(['xticklabels', 'yticklabels'], x_labels, y_labels))


@savefig
def plot_clustermap(data, x_labels=None, y_labels=None, cmap='purple'):
    """Plot clustermap.

    Parameters
    ----------
    data : 2d array
        Data to plot, as a clustermap.
    cmap : matplotlib.cmap
        Colormap to use for the plot.
    x_labels : list of str
        Labels for the x-axis.
    y_labels : list of str
        Labels for the y-axis.
    """

    sns.set()
    sns.set_context("paper", font_scale=1.5)

    if isinstance(cmap, str):
        cmap = get_cmap(cmap)

    cg = sns.clustermap(data, cmap=cmap, method='complete', metric='cosine',
                        **check_args(['xticklabels', 'yticklabels'], x_labels, y_labels))


    cg.cax.set_visible(True)
    _ = plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=60, ha='right')
    _ = plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)


@savefig
def plot_dendrogram(data, labels=None, ax=None):
    """Plot dendrogram.

    Parameters
    ----------
    dat : 2d array
        Data to plot, as a dendrogram.
    labels : list of str, optional
        Labels for the dendrogram.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    """

    linkage_data = hier.linkage(data, method='complete', metric='cosine')

    hier.dendrogram(linkage_data, orientation='left', color_threshold=0.25,
                    leaf_font_size=12, ax=check_ax(ax, (3, 15)), **check_args(['labels'], labels))
