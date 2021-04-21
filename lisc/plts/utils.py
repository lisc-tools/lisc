"""Plot utilities."""

import os
from functools import wraps

from lisc import Counts
from lisc.utils.db import SCDB
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')
sns = safe_import('seaborn')

###################################################################################################
###################################################################################################

def check_args(names, *inputs):
    """Checks a series of inputs, and renames them and packages them, if they are not None.

    Parameters
    ----------
    names : list of str
        List of names to apply to the given inputs.
    *inputs
        Any input variables to check.

    Returns
    -------
    dict
        A dictionary with the new names and values, for all inputs that are not None.
    """

    return {label : value for label, value in zip(names, inputs) if value is not None}


def check_aliases(kwargs, aliases, default=None):
    """Check a dictionary input for a list of potential key aliases.

    Parameters
    ----------
    kwargs : dict
        Dictionary to check for elements labelled with possible aliases.
    aliases : list
        List of possible key value labels.
    default
        Default value to return if none of the potential labels are present.

    Returns
    -------
    value
        The value of the extracted label, or None if no given labels are present.
    """

    value = default
    for alias in aliases:
        if alias in kwargs:
            value = kwargs.pop(alias)
            break

    return value


def get_cmap(cmap):
    """Get a requested colormap.

    Parameters
    ----------
    cmap : {'purple', 'blue'}
        Specifier for which colormap to use.

    Returns
    -------
    cmap : matplotlib.cmap
        The specified colormap object.
    """

    if cmap == 'purple':
        cmap = sns.cubehelix_palette(as_cmap=True)
    elif cmap == 'blue':
        cmap = sns.cubehelix_palette(as_cmap=True, rot=-.3, light=0.9, dark=0.2)
    else:
        raise ValueError('Requested colormap not understood.')

    return cmap


def counts_data_helper(data, x_labels, y_labels, attribute, transpose):
    """A helper function for checking data inputs for counts plots.

    Parameters
    ----------
    data : Counts or 2d array
        Data to plot in matrix format.
    x_labels, y_labels : list of str
        Labels for the axes.
    attribute : {'score', 'counts'}
        Which data attribute from the data object to extract.
    transpose : bool
        Whether to transpose the data.

    Returns
    -------
    data : 2d array
        Array of data to plot.
    x_labels, y_labels : list of str
        Labels for the axes
    """

    if isinstance(data, Counts):

        if attribute == 'score' and data.score_info.get('type') in ['similarity']:

            x_labels = y_labels = data.terms[data.score_info['dim']].labels

        else:
            if data.square:
                x_dim, y_dim = ['A', 'A']
            else:
                x_dim, y_dim = ['B', 'A'] if not transpose else ['A', 'B']

            x_labels = data.terms[x_dim].labels if not x_labels else x_labels
            y_labels = data.terms[y_dim].labels if not y_labels else y_labels

        data = getattr(data, attribute)

    if transpose:
        data = data.T

    return data, x_labels, y_labels


def check_ax(ax, figsize=None):
    """Check whether a figure axes object is defined, define if given a figsize.

    Parameters
    ----------
    ax : matplotlib.Axes or None
        Axes object to check if is defined.
    figsize : (float, float)
        The figure size for a new axis, if ax is not defined.

    Returns
    -------
    ax : matplotlib.Axes or None
        Figure axes object to use.
    """

    if not ax and figsize:
        _, ax = plt.subplots(figsize=figsize)

    return ax


def savefig(func):
    """Decorator to save out a figure, if requested."""

    @wraps(func)
    def decorated(*args, **kwargs):

        save_fig = kwargs.pop('save_fig', False)
        file_name = kwargs.pop('file_name', None)
        file_path = kwargs.pop('directory', None)
        close = kwargs.pop('close', None)
        transparent = kwargs.pop('transparent', False)

        if isinstance(f_path, SCDB):
            f_path = f_path.get_folder_path('figures')

        func(*args, **kwargs)

        if save_fig:
            full_path = os.path.join(file_path, file_name) if file_path else file_name
            plt.savefig(full_path, bbox_inches='tight', transparent=transparent)

        if close:
            plt.close()

    return decorated
