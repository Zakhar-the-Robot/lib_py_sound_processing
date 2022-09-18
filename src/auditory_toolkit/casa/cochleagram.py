##############################################################
# Zakhar-the-Robot - Auditory Toolkit, Nikita Mortuzaiev, 2022
##############################################################
"""Contains functions for cochleagram computing."""

from typing import Tuple, Union

import numpy as np
from brian2 import Hz, kHz
from brian2hears import erbspace, FunctionFilterbank, Gammatone, Sound


def cochlea(sound: Sound,
            n_channels: int = 128,
            min_freq: float = 20*Hz,
            max_freq: float = 20*kHz,
            return_cf: bool = False) -> Union[Tuple, FunctionFilterbank]:
    """Return a model of human cochlea.

    :param Sound sound: Input sound
    :param int n_channels: Number of frequency channels in the output cochleagram
    :param float min_freq: Lowest center frequency value for the gammatone filterbank (default is 20 Hz)
    :param float max_freq: Highest center frequency value for the gammatone filterbank (default is 20 kHz)
    :param bool return_cf: If True, also returns center frequencies of the gammatone filters
    :returns: Filterbank representing human basilar membrane
    :rtype: Union[tuple, FunctionFilterbank]

    """
    n_channels = int(n_channels)
    min_freq = float(min_freq) * Hz
    max_freq = float(max_freq) * Hz

    # Center frequencies on the ERB scale
    center_freqs = erbspace(min_freq, max_freq, n_channels)

    # Gammatone filterbank
    gammatone = Gammatone(sound, center_freqs)

    # Half-wave rectification + square root function to amplify low amplitudes
    cochlea_ = FunctionFilterbank(gammatone, lambda x: np.clip(x, 0, np.Inf) ** (1.0 / 2.0))

    if return_cf:
        return cochlea_, center_freqs
    else:
        return cochlea_


def cochleagram(sound: Sound,
                n_channels: int = 128,
                min_freq: float = 20*Hz,
                max_freq: float = 20*kHz,
                return_cf: bool = False) -> Union[Tuple, np.ndarray]:
    """Compute a cochleagram from the input sound.

    :param Sound sound: Input sound
    :param int n_channels: Number of frequency channels in the output cochleagram
    :param float min_freq: Lowest center frequency value for the gammatone filterbank (default is 20 Hz)
    :param float max_freq: Highest center frequency value for the gammatone filterbank (default is 20 kHz)
    :param bool return_cf: If True, also returns center frequencies of the gammatone filters
    :returns: Cochleagram
    :rtype: Union[tuple, np.ndarray]

    """
    # Get the cochlea model
    cochlea_, center_freqs = cochlea(sound, n_channels, min_freq, max_freq, return_cf=True)

    # Do the computations
    cochleagram_ = cochlea_.process().T

    if return_cf:
        return cochleagram_, center_freqs
    else:
        return cochleagram_
