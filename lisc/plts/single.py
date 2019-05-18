"""LISC plots - plots for single terms."""

import os

import matplotlib.pyplot as plt

from lisc.core.db import check_db

#########################################################################################
#########################################################################################

def plot_years(year_counts, label, disp_fig=True, save_fig=False, db=None):
    """Plot publications across years histogram."""

    f, ax = plt.subplots(figsize=(10, 5))

    yrs = set(range(1985, 2016))

    # Extract x & y data to plot
    x_dat = [y[0] for y in year_counts]
    y_dat = [y[1] for y in year_counts]

    # Add line and points to plot
    plt.plot(x_dat, y_dat)
    plt.plot(x_dat, y_dat, '.', markersize=16)

    # Set plot limits
    plt.xlim([min(yrs), max(yrs)])
    plt.ylim([0, max(y_dat)+5])

    # Add title & labels
    plt.title('Publication History', fontsize=24, fontweight='bold')
    plt.xlabel('Year', fontsize=18)
    plt.ylabel('# Pubs', fontsize=18)

    if save_fig:

        db = check_db(db)
        s_file = os.path.join(db.figs_path, 'year', label + '.svg')

        plt.savefig(s_file, transparent=True)
        if not disp_fig:
            plt.close()
