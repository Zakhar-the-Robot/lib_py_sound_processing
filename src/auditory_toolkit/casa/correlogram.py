##############################################################
# Zakhar-the-Robot - Auditory Toolkit, Nikita Mortuzaiev, 2022
##############################################################
"""Contains functions for correlogram computing."""

from typing import Optional

# import numpy as np
# from statsmodels.tsa.stattools import acf
from brian2 import check_units
from brian2hears import Bufferable, FunctionFilterbank


class AutocorrelationFilterbank(FunctionFilterbank):

    """Apply the autocorrelation function to the given source."""

    @check_units(n_lags=1)
    def __init__(self, source: Bufferable, n_lags: Optional[int] = None):
        # TODO
        FunctionFilterbank.__init__(self, source, self.func, n_lags=n_lags)

    # TODO: Will not work - need to write the ACF function for my specific needs?
    # @staticmethod
    # def func(source, n_lags):
    #     return np.apply_along_axis(lambda vec: acf(vec, nlags=n_lags), 0, source.buffer_fetch_next(aaaaa))
    #
    # def buffer_fetch_next(self, samples):
    #     start = self.next_sample
    #     self.next_sample += samples
    #     end = start+samples
    #     input = self.source.buffer_fetch(start, end)
    #     return self.buffer_apply(input)
