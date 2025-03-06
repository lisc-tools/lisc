"""Plots for counts data.

Notes
-----
The functions here serve as wrappers on external plotting and analysis
libraries, to give access to relevant plots and clustering measures.
"""

import numpy as np

from lisc import Counts1D, Counts
from lisc.plts.utils import (check_args, check_ax, savefig, get_cmap,
                             counts_data_helper, rotate_ticks)
from lisc.modutils.dependencies import safe_import

plt = safe_import('.pyplot', 'matplotlib')
sns = safe_import('seaborn')
hier = safe_import('.cluster.hierarchy', 'scipy')

###################################################################################################
###################################################################################################

@savefig
def plot_matrix(data, x_labels=None, y_labels=None, attribute='score', transpose=False,
                cmap='purple', square=False, ax=None, **kwargs):
    """Plot a matrix as a heatmap.

    Parameters
    ----------
    data : Counts or 2d array
        Data to plot in matrix format.
    x_labels : list of str, optional
        Labels for the x-axis.
    y_labels : list of str, optional
        Labels for the y-axis.
    attribute : {'score', 'counts'}, optional
        Which data attribute from the counts object to plot the data for.
        Only used if the `data` input is a Counts object.
    transpose : bool, optional, default: False
        Whether to transpose the data before plotting.
    cmap : {'purple', 'blue'} or matplotlib.cmap
        Colormap to use for the plot.
        If string, uses a sequential palette of the specified color.
    square : bool, optional, default: False
        Whether to plot all the cells as equally sized squares.
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

    rot_kwargs = {'xtickrotation' : kwargs.pop('xtickrotation', None),
                  'ytickrotation' : kwargs.pop('ytickrotation', None)}

    if isinstance(cmap, str):
        cmap = get_cmap(cmap)

    data, x_labels, y_labels = counts_data_helper(data, x_labels, y_labels, attribute, transpose)

    with sns.plotting_context("notebook", font_scale=kwargs.pop('font_scale', 1.0)):
        ax = check_ax(ax, kwargs.pop('figsize', None))
        sns.heatmap(data, square=square, cmap=cmap, ax=ax, **kwargs,
                    **check_args(['xticklabels', 'yticklabels'], x_labels, y_labels))

    rotate_ticks(ax if ax else plt.gca(), **rot_kwargs)

    plt.tight_layout()


@savefig
def plot_vector(data, dim='A', labels=None, transpose=False, cmap='purple', ax=None, **kwargs):
    """Plot a vector as an annotated heatmap.

    Parameters
    ----------
    data : Counts1D or Counts or 1d array
        Data to plot as a heatmap.
    dim : {'A', 'B'}, optional
        Which set of terms to plot.
        Only used if `data` is a `Counts` object.
    labels : list of str, optional
        Labels for the figure.
    transpose : bool, optional, default: False
        Whether to transpose the data before plotting.
    cmap : {'purple', 'blue'} or matplotlib.cmap
        Colormap to use for the plot.
        If string, uses a sequential palette of the specified color.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    **kwargs
        Additional keyword arguments to pass through to seaborn.heatmap.
    """

    rot_kwargs = {'xtickrotation' : kwargs.pop('xtickrotation', None),
                  'ytickrotation' : kwargs.pop('ytickrotation', None)}

    if isinstance(cmap, str):
        cmap = get_cmap(cmap)

    if isinstance(data, Counts1D):
        data = data.counts
    elif isinstance(data, Counts):
        data = data.terms[dim].counts

    if data.ndim == 1:
        data = np.expand_dims(data, 1)
    if transpose:
        data = data.T

    label_kwargs = {'xticklabels' : kwargs.pop('xticklabels', []),
                    'yticklabels' : kwargs.pop('yticklabels', [])}
    if labels and transpose:
        label_kwargs['xticklabels'] = labels
    elif labels:
        label_kwargs['yticklabels'] = labels

    ax = check_ax(ax, kwargs.pop('figsize', None))
    sns.heatmap(data, cmap=cmap, square=kwargs.pop('square', True),
                annot=kwargs.pop('annot', True), fmt=kwargs.pop('fmt', 'd'),
                annot_kws={"size": 18}, cbar=kwargs.pop('cbar', False),
                ax=ax, **label_kwargs, **kwargs)

    rotate_ticks(ax if ax else plt.gca(), **rot_kwargs)


@savefig
def plot_clustermap(data, x_labels=None, y_labels=None, attribute='score', transpose=False,
                    method='complete', metric='cosine', cmap='purple', **kwargs):
    """Plot a clustermap of the given data.

    Parameters
    ----------
    data : Counts or 2d array
        Data to plot, as a clustermap.
    x_labels : list of str, optional
        Labels for the x-axis.
    y_labels : list of str, optional
        Labels for the y-axis.
    attribute : {'score', 'counts'}, optional
        Which data attribute from the counts object to plot the data for.
        Only used if the `data` input is a Counts object.
    transpose : bool, optional, default: False
        Whether to transpose the data before plotting.
    method : str, optional, default: 'complete'
        The linkage algorithm to use. See `scipy.cluster.hierarchy.linkage` for options.
    metric : str or function, optional, default: 'cosine'
        The distance metric to use. See `scipy.spatial.distance.pdist` for options.
    cmap : {'purple', 'blue'} or matplotlib.cmap
        Colormap to use for the plot.
        If string, uses a sequential palette of the specified color.
    **kwargs
        Additional keyword arguments to pass through to seaborn.clustermap.

    Notes
    -----
    This function is a wrapper of the `seaborn.clustermap` plot function.

    Examples
    --------
    See the example for the :meth:`~.compute_score` method of the :class:`~.Counts` class.
    """

    if isinstance(cmap, str):
        cmap = get_cmap(cmap)

    data, x_labels, y_labels = counts_data_helper(data, x_labels, y_labels, attribute, transpose)

    with sns.plotting_context("notebook", font_scale=kwargs.pop('font_scale', 1.0)):
        cg = sns.clustermap(data, method=method, metric=metric,
                            cmap=cmap, figsize=kwargs.pop('figsize', None),
                            **check_args(['xticklabels', 'yticklabels'], x_labels, y_labels),
                            **kwargs)

    _ = plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=60, ha='right')
    _ = plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)


@savefig
def plot_dendrogram(data, labels=None, attribute='score', transpose=False,
                    method='complete', metric='cosine', ax=None, **kwargs):
    """Plot a dendrogram of the given data based on hierarchical clustering.

    Parameters
    ----------
    data : Counts or 2d array
        Data to plot in a dendrogram.
    labels : list of str, optional
        Labels for the dendrogram.
    attribute : {'score', 'counts'}, optional
        Which data attribute from the counts object to plot the data for.
        Only used if the `data` input is a Counts object.
    transpose : bool, optional, default: False
        Whether to transpose the data before plotting.
    method : str, optional, default: 'complete'
        The linkage algorithm to use. See `scipy.cluster.hierarchy.linkage` for options.
    metric : str or function, optional, default: 'cosine'
        The distance metric to use.  See `scipy.spatial.distance.pdist` for options.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    **kwargs
        Additional keyword arguments to pass through to scipy.cluster.hierarchy.dendrogram.

    Notes
    -----
    This function is a wrapper of the `scipy.cluster.hierarchy.dendrogram' plot function.

    Examples
    --------
    See the example for the :meth:`~.compute_score` method of the :class:`~.Counts` class.
    """

    if isinstance(data, Counts):
        labels = data.terms['A' if not transpose else 'B'].labels
        data = getattr(data, attribute).T if transpose else getattr(data, attribute)

    linkage_data = hier.linkage(data, method=method, metric=metric)

    with sns.plotting_context("notebook", font_scale=kwargs.pop('font_scale', 1.0)):
        hier.dendrogram(linkage_data,
                        orientation=kwargs.pop('orientation', 'left'),
                        color_threshold=kwargs.pop('color_threshold', 0.25),
                        leaf_font_size=kwargs.pop('leaf_font_size', 12),
                        ax=check_ax(ax, kwargs.pop('figsize', None)),
                        **check_args(['labels'], labels),
                        **kwargs)
    plt.tight_layout()
