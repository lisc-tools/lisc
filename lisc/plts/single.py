"""LISC plots - plots for single terms."""

import os

import matplotlib.pyplot as plt

from lisc.core.db import check_db
from lisc.plts.utils import _save_fig

###################################################################################################
###################################################################################################

def plot_years(year_counts, label=None, year_range=None, save_fig=False):
    """Plot publications across years histogram.

    Parameters
    ----------
    year_counts : xx
        xx
    label : xx
        xx
    year_range : xx
        xx
    save_fig : xx
        xx
    """

    # Extract x & y data to plot
    x_dat = [xd[0] for xd in year_counts]
    y_dat = [yd[1] for yd in year_counts]

    f, ax = plt.subplots(figsize=(10, 5))

    # Add line and points to plot
    plt.plot(x_dat, y_dat)
    plt.plot(x_dat, y_dat, '.', markersize=16)

    # Set plot limits
    if year_range:
        plt.xlim([year_range[0], year_range[1]])
    plt.ylim([0, max(y_dat)+5])

    # Add title & labels
    plt.title('Publication History', fontsize=24, fontweight='bold')
    plt.xlabel('Year', fontsize=18)
    plt.ylabel('# Pubs', fontsize=18)

    _save_fig(save_fig, label)
