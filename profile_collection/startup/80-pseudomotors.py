from ophyd import (EpicsMotor, PseudoPositioner, PseudoSingle)
from ophyd import Component as Cpt


class SamplePositioner(PseudoPositioner):
    '''
    Maintains an offset between a master/slave set of positioners
    such that the slave movement is the negative of the master's relative
    motion (i.e. maintains constant, negative, relative offset).
    Assumes that the user has adjusted the axes to their initial positions.

    Example
    -------------
    psamp_x = SamplePositioner(prefix='', name='psamp_x', concurrent=True)
    '''
    physical_sample_holder = Cpt(EpicsMotor, '...')
    beamstop = Cpt(EpicsMotor, '...')
    sample_holder = Cpt(PseudoSingle, '...')

    def forward(self, pos):
        "pos is a self.PseudoPosition"
        delta = pos - pos.sample_holder.pos
        return self.RealPosition(physical_sample_holder=pos.sample_holder,
                                 beamstop=self.beamstop.position - delta)

    def reverse(self, pos):
        "pos is self.RealPosition"
        return self.PsuedoPosition(sample_holder=pos.physical_sample_holder)


psamp_x = SamplePositioner(prefix='', name='psamp_x', concurrent=True)
