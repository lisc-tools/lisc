"""LISC plots - plots for group analysis."""

import os

import seaborn as sns
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hier

from lisc.core.db import check_db
from lisc.plts.utils import _save_fig

###################################################################################################
###################################################################################################

def plot_matrix(dat, x_labels, y_labels, square=False, figsize=(10, 12),
                save_fig=False, save_name='Matrix'):
    """Plot the matrix of percent asscociations between terms.

    Parameters
    ----------
    dat : xx
        xx
    x_labels : xx
        xx
    y_labels : xx
        xx
    square : xx
        xx
    """

    f, ax = plt.subplots(figsize=figsize)

    sns.heatmap(dat, square=square, xticklabels=x_labels, yticklabels=y_labels)

    f.tight_layout()

    _save_fig(save_fig, save_name)


def plot_clustermap(dat, cmap='purple', save_fig=False, save_name='Clustermap'):
    """Plot clustermap.

    Parameters
    ----------
    dat : pandas.DataFrame
        Data to create clustermap from.
    cmap : xx
        xx
    save_fig : xx
        xx
    save_name : xx
        xx
    """

    # Set up plotting and aesthetics
    sns.set()
    sns.set_context("paper", font_scale=1.5)

    # Set colourmap
    if cmap == 'purple':
        cmap = sns.cubehelix_palette(as_cmap=True)
    elif cmap == 'blue':
        cmap = sns.cubehelix_palette(as_cmap=True, rot=-.3, light=0.9, dark=0.2)

    # Create the clustermap
    cg = sns.clustermap(dat, cmap=cmap, method='complete', metric='cosine', figsize=(12, 10))

    # Fix axes
    cg.cax.set_visible(True)
    _ = plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=60, ha='right')
    _ = plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)

    _save_fig(save_fig, save_name)


def plot_dendrogram(dat, labels, save_fig=False, save_name='Dendrogram'):
    """Plot dendrogram.

    Parameters
    ----------
    dat :
        xx
    labels :
        xx
    save_fig :
        xx
    save_name :
        xx
    """

    plt.figure(figsize=(3, 15))

    linkage_data = hier.linkage(dat, method='complete', metric='cosine')

    dendro_plot = hier.dendrogram(linkage_data, orientation='left', labels=labels,
                                  color_threshold=0.25, leaf_font_size=12)

    _save_fig(save_fig, save_name)
