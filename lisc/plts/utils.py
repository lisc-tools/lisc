"""LISC plots - utilities."""

import os

import matplotlib.pyplot as plt

#from lisc.core.db import check_db

###################################################################################################
###################################################################################################

def _save_fig(save_fig, save_name, save_folder=None):
    """


    """

    if save_fig:

        save_file = os.path.join(save_folder, save_name + '.png')
        plt.savefig(save_file, transparent=True)
