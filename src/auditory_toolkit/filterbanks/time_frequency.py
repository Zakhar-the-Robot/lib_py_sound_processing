##############################################################
# Zakhar-the-Robot - Auditory Toolkit, Nikita Mortuzaiev, 2022
##############################################################

from brian2hears import Bufferable, FunctionFilterbank


class ThresholdFilterbank(FunctionFilterbank):

    """Filterbank that returns boolean values depending on the input exceeding certain threshold."""

    def __init__(self,
                 source: Bufferable,
                 threshold: float):
        self.threshold = threshold
        FunctionFilterbank.__init__(self, source, lambda src: src > threshold)
