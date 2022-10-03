##############################################################
# Zakhar-the-Robot - Auditory Toolkit, Nikita Mortuzaiev, 2022
##############################################################
"""Contains functions for plotting."""

from typing import Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt


def plot_cochleagram(cochleagram: np.ndarray,
                     samplerate: int,
                     # antialiasing_factor: Optional[int] = None,
                     fig_title: str = "Cochleagram",
                     fig_size: Tuple[int] = (12, 7),
                     save_fig_path: Optional[str] = None):
    """Plot a cochleagram.

    :param np.ndarray cochleagram: Input cochleagram
    :param int samplerate: Samplerate of the input sound
    :param str fig_title: Title of the plot
    :param tuple fig_size: Size of the matplotlib figure
    :param Optional[str] save_fig_path: Path to the output file

    """
    # if antialiasing_factor is not None:
    #     rms = _decrease_time_resolution(cochleagram, samplerate)

    # TODO: Adjust? What about antialiasing? Probably just rewrite...

    fig = plt.figure(figsize=fig_size)
    img = plt.imshow(cochleagram, origin='lower', aspect='auto', vmin=0,
                     extent=[0, cochleagram.shape[1] / samplerate, 0, cochleagram.shape[0]])
    plt.colorbar(img)

    plt.title(fig_title, fontsize=14)
    plt.xlabel("Time (s)", fontsize=14)
    plt.ylabel("Frequency Channels", fontsize=14)

    if save_fig_path is not None:
        fig.savefig(save_fig_path, bbox_inches='tight', dpi=384)

    plt.tight_layout()
    plt.show()

