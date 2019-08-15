"""LISC plots - plots for counts data.

Notes
-----
The functions here serve as wrappers on external plotting and analysis
libraries, to give access to relevant plots and clustering measures.
"""

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

    Notes
    -----
    This function is a wrapper on the seaborn `heatmap` plot function.
    """

    sns.heatmap(data, square=square, ax=check_ax(ax),
                **check_args(['xticklabels', 'yticklabels'], x_labels, y_labels))
    plt.tight_layout()


@savefig
def plot_clustermap(data, x_labels=None, y_labels=None, cmap='purple'):
    """Plot clustermap.

    Parameters
    ----------
    data : 2d array
        Data to plot, as a clustermap.
    x_labels : list of str
        Labels for the x-axis.
    y_labels : list of str
        Labels for the y-axis.
    cmap : matplotlib.cmap
        Colormap to use for the plot.

    Notes
    -----
    This function is a wrapper on the seaborn `clustermap` plot function.
    """

    sns.set()
    sns.set_context("paper", font_scale=1.5)

    if isinstance(cmap, str):
        cmap = get_cmap(cmap)

    cg = sns.clustermap(data, cmap=cmap, method='complete', metric='cosine',# figsize=(8, 8),
                        **check_args(['xticklabels', 'yticklabels'], x_labels, y_labels))

    _ = plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=60, ha='right')
    _ = plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)

    cg.fig.subplots_adjust(bottom=0.25)
    cg.fig.subplots_adjust(right=0.75)


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

    Notes
    -----
    This function is a wrapper on the scipy `dendrogram` plot function.
    """

    linkage_data = hier.linkage(data, method='complete', metric='cosine')

    hier.dendrogram(linkage_data, orientation='left', color_threshold=0.25,
                    leaf_font_size=12, ax=check_ax(ax), **check_args(['labels'], labels))
    plt.tight_layout()
