"""Plot utilities."""

from functools import wraps
from os.path import join as pjoin

from lisc import Counts
from lisc.io.db import SCDB
from lisc.modutils.dependencies import safe_import

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
    default : object or None, optional
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
    figsize : (float, float), optional
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

        # Grab file name and path arguments, if they are in kwargs
        file_name = kwargs.pop('file_name', None)
        file_path = kwargs.pop('directory', None)

        # Check for an explicit argument for whether to save figure or not
        #   Defaults to saving when file name given (since bool(str)->True; bool(None)->False)
        save_fig = kwargs.pop('save_fig', bool(file_name))

        # Check any collect any other plot keywords
        save_kwargs = kwargs.pop('save_kwargs', {})
        save_kwargs.setdefault('bbox_inches', 'tight')

        # Check and collect whether to close the plot
        close = kwargs.pop('close', False)

        if isinstance(file_path, SCDB):
            file_path = file_path.get_folder_path('figures')

        func(*args, **kwargs)

        if save_fig:
            save_figure(file_name, file_path, close, **save_kwargs)

    return decorated


def save_figure(file_name, file_path=None, close=False, **save_kwargs):
    """Save out a figure.

    Parameters
    ----------
    file_name : str
        File name for the figure file to save out.
    file_path : str or Path, optional
        Path for where to save out the figure to.
    close : bool, optional, default: False
        Whether to close the plot after saving.
    save_kwargs
        Additional arguments to pass into the save function.
    """

    full_path = pjoin(file_path, file_name) if file_path else file_name
    plt.savefig(full_path, **save_kwargs)

    if close:
        plt.close()


def rotate_ticks(ax, xtickrotation=None, ytickrotation=None):
    """Rotate ticklabels on a plot.

    Parameters
    ----------
    ax : matplotlib.Axes
        Figure axes to apply tick rotation to.
    xtickrotation, ytickrotation : float, optional
        Rotation to apply to the x and/or y axis tick labels.
    """

    if xtickrotation:
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ax.get_xticklabels(),
                           rotation=xtickrotation,
                           horizontalalignment='right')

    if ytickrotation:
        alignment = 'top' if ytickrotation > 0 and ytickrotation < 180 else 'bottom'
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ax.get_yticklabels(),
                           rotation=ytickrotation,
                           verticalalignment=alignment)
