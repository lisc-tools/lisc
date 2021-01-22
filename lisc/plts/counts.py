"""Plots for counts data.

Notes
-----
The functions here serve as wrappers on external plotting and analysis
libraries, to give access to relevant plots and clustering measures.
"""

from lisc import Counts
from lisc.plts.utils import check_args, check_ax, savefig, get_cmap, counts_data_helper
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')
sns = safe_import('seaborn')
hier = safe_import('.cluster.hierarchy', 'scipy')

###################################################################################################
###################################################################################################

@savefig
def plot_matrix(data, x_labels=None, y_labels=None, cmap='purple', square=False,
                attribute='score', transpose=False, ax=None, **kwargs):
    """Plot a matrix representation of given data.

    Parameters
    ----------
    data : Counts or 2d array
        Data to plot in matrix format.
    x_labels : list of str, optional
        Labels for the x-axis.
    y_labels : list of str, optional
        Labels for the y-axis.
    cmap : {'purple', 'blue'} or matplotlib.cmap
        Colormap to use for the plot.
        If string, uses a sequential palette of the specified color.
    square : bool
        Whether to plot all the cells as equally sized squares.
    attribute : {'score', 'counts'}, optional
        Which data attribute from the counts object to plot the data for.
        Only used if the `data` input is a Counts object.
    transpose : bool, optional, default: False
        Whether to transpose the data before plotting.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    **kwargs
        Additional keyword arguments to pass through to seaborn.heatmap.

    Notes
    -----
    This function is a wrapper of the seaborn `heatmap` plot function.

    Examples
    --------
    See the example for the :meth:`~.compute_score` method of the :class:`~.Counts` class.
    """

    if isinstance(cmap, str):
        cmap = get_cmap(cmap)

    data, x_labels, y_labels = counts_data_helper(data, x_labels, y_labels,  attribute, transpose)

    sns.heatmap(data, square=square, ax=check_ax(ax), cmap=cmap,
                **check_args(['xticklabels', 'yticklabels'], x_labels, y_labels), **kwargs)
    plt.tight_layout()


@savefig
def plot_clustermap(data, x_labels=None, y_labels=None, cmap='purple',
                    attribute='score', transpose=False, **kwargs):
    """Plot a clustermap of the given data.

    Parameters
    ----------
    data : Counts or 2d array
        Data to plot, as a clustermap.
    x_labels : list of str, optional
        Labels for the x-axis.
    y_labels : list of str, optional
        Labels for the y-axis.
    cmap : {'purple', 'blue'} or matplotlib.cmap
        Colormap to use for the plot.
        If string, uses a sequential palette of the specified color.
    attribute : {'score', 'counts'}, optional
        Which data attribute from the counts object to plot the data for.
        Only used if the `data` input is a Counts object.
    transpose : bool, optional, default: False
        Whether to transpose the data before plotting.
    **kwargs
        Additional keyword arguments to pass through to seaborn.clustermap.

    Notes
    -----
    This function is a wrapper of the seaborn `clustermap` plot function.

    Examples
    --------
    See the example for the :meth:`~.compute_score` method of the :class:`~.Counts` class.
    """

    sns.set()
    sns.set_context("paper", font_scale=1.5)

    if isinstance(cmap, str):
        cmap = get_cmap(cmap)

    data, x_labels, y_labels =  counts_data_helper(data, x_labels, y_labels, attribute, transpose)

    cg = sns.clustermap(data, cmap=cmap, method='complete', metric='cosine',
                        **check_args(['xticklabels', 'yticklabels'], x_labels, y_labels),
                        **kwargs)

    _ = plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=60, ha='right')
    _ = plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)

    cg.fig.subplots_adjust(bottom=0.25)
    cg.fig.subplots_adjust(right=0.75)


@savefig
def plot_dendrogram(data, labels=None, ax=None):
    """Plot a dendrogram of the given data.

    Parameters
    ----------
    data : Counts or 2d array
        Data to plot in a dendrogram.
    labels : list of str, optional
        Labels for the dendrogram.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    **kwargs
        Additional keyword arguments to pass through to scipy.cluster.hierarchy.

    Notes
    -----
    This function is a wrapper of the scipy `dendrogram` plot function.

    Examples
    --------
    See the example for the :meth:`~.compute_score` method of the :class:`~.Counts` class.
    """

    if isinstance(data, Counts):
        labels = data.terms['B' if not transpose else 'A'].labels
        data = getattr(data, attribute).T if transpose else getattr(data, attribute)

    linkage_data = hier.linkage(data, method='complete', metric='cosine')

    hier.dendrogram(linkage_data, orientation='left', color_threshold=0.25,
                    leaf_font_size=12, ax=check_ax(ax), **check_args(['labels'], labels))
    plt.tight_layout()
