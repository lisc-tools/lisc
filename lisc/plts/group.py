"""LISC plots - plots for group analysis."""

from lisc.plts.utils import check_ax, savefig
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')
sns = safe_import('seaborn')
hier = safe_import('.cluster.hierarchy', 'scipy')

###################################################################################################
###################################################################################################

@savefig
def plot_matrix(dat, x_labels, y_labels, square=False, ax=None):
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

    ax = check_ax(ax, (10, 12))
    sns.heatmap(dat, square=square, xticklabels=x_labels, yticklabels=y_labels, ax=ax)

    #ax.tight_layout()


@savefig
def plot_clustermap(dat, cmap='purple', ax=None):
    """Plot clustermap.

    Parameters
    ----------
    dat : xx
        xx
    cmap : xx
        xx
    """

    # Set up plotting and aesthetics
    sns.set()
    sns.set_context("paper", font_scale=1.5)

    ax = check_ax(ax, (12, 10))

    # Set colourmap
    if cmap == 'purple':
        cmap = sns.cubehelix_palette(as_cmap=True)
    elif cmap == 'blue':
        cmap = sns.cubehelix_palette(as_cmap=True, rot=-.3, light=0.9, dark=0.2)

    # Create the clustermap
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
    dat :
        xx
    labels :
        xx
    """

    ax = check_ax(ax, (3, 15))

    linkage_data = hier.linkage(dat, method='complete', metric='cosine')

    dendro_plot = hier.dendrogram(linkage_data, orientation='left', labels=labels,
                                  color_threshold=0.25, leaf_font_size=12, ax=ax)
