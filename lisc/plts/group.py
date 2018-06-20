"""Create data plots for LISC - plots for group analysis."""

import os
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hier

from lisc.core.db import check_db

#########################################################################################
#########################################################################################

def plot_matrix(dat, x_labels, y_labels, square=False, figsize=(10, 12), save_fig=False, save_name='Matrix'):
    """Plot the matrix of percent asscociations between terms."""

    f, ax = plt.subplots(figsize=figsize)

    sns.heatmap(dat, square=square, xticklabels=x_labels, yticklabels=y_labels)

    f.tight_layout()

    # Save out - if requested
    if save_fig:

        db = check_db(db)
        s_file = os.path.join(db.figs_path, save_name + '.svg')

        plt.savefig(s_file)


def plot_clustermap(dat, cmap='purple', save_fig=False, save_name='Clustermap'):
    """Plot clustermap.

    Parameters
    ----------
    dat : pandas.DataFrame
        Data to create clustermap from.
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

    # Save out - if requested
    if save_fig:

        db = check_db(db)
        s_file = os.path.join(db.figs_path, save_name + '.svg')

        cg.savefig(s_file, transparent=True)


def plot_dendrogram(dat, labels, save_fig=False, save_name='Dendrogram'):
    """Plot dendrogram."""

    plt.figure(figsize=(3, 15))

    Y = hier.linkage(dat, method='complete', metric='cosine')

    Z = hier.dendrogram(Y, orientation='left', labels=labels,
                        color_threshold=0.25, leaf_font_size=12)

    # Save out - if requested
    if save_fig:

        db = check_db(db)
        s_file = os.path.join(db.figs_path, save_name + '.svg')

        cg.savefig(s_file, transparent=True)
