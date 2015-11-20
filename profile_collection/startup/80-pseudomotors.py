from ophyd.controls import (EpicsMotor, PseudoPositioner)


class SamplePositioner(PseudoPositioner):
    '''Maintains an offset between a master/slave set of positioners
       such that the slave movement is the negative of the master's relative
       motion (i.e. maintains constant, negative, relative offset).

       Assumes that the user has adjusted the axes to their initial positions.

       Example
       -------------
       pseudo_master = SamplePositioner("pmaster", [real_master, real_slave],
                                        concurrent=True)
    '''

    def _calc_forward(self, *args, pseudo=None, **kwargs):
        delta = -(pseudo - self['pseudo'].position)
        return [pseudo, self._real[1].position + delta]

    def _calc_reverse(self, *args, **kwargs):
        return [self._real[0].position]


# NOTE: assumes sam_x and sambst_x are accessible from ipython's namespace
psamp_x = SamplePositioner('psamp_x', [sam_x, sambst_x], concurrent=True)
