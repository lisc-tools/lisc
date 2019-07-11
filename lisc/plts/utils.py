"""LISC plots - utilities."""

import os
from functools import wraps

from lisc.core.db import SCDB
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')
sns = safe_import('seaborn')

###################################################################################################
###################################################################################################

def get_cmap(cmap):
    """Get a requested colormap.

    Parameters
    ----------
    cmap : {'purple', 'blue'}
        xx

    Returns
    -------
    cmap : xx
        xx
    """

    if cmap == 'purple':
        cmap = sns.cubehelix_palette(as_cmap=True)
    elif cmap == 'blue':
        cmap = sns.cubehelix_palette(as_cmap=True, rot=-.3, light=0.9, dark=0.2)

    return cmap


def check_ax(ax, figsize=None):
    """Check whether a figure axes object is defined, define if not.

    Parameters
    ----------
    ax : matplotlib.Axes or None
        Axes object to check if is defined.

    Returns
    -------
    ax : matplotlib.Axes
        Figure axes object to use.
    """

    if not ax:
        _, ax = plt.subplots(figsize=figsize)

    return ax


def savefig(func):
    """Decorator to save out a figure, if requested."""

    @wraps(func)
    def decorated(*args, **kwargs):

        save_fig = kwargs.pop('save_fig', False)
        f_name = kwargs.pop('f_name', None)
        f_path = kwargs.pop('folder', None)

        if isinstance(f_path, SCDB):
            f_path = f_path.figures_path

        func(*args, **kwargs)

        if save_fig:
            full_path = os.path.join(f_path, f_name) if f_path else f_name
            plt.savefig(full_path)

    return decorated
