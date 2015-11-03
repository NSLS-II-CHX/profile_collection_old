from ophyd.controls import EpicsMotor

class ReversedEpicsMotor(EpicsMotor):
    
	def move(self, position, wait=True, **kwargs):
		return super().move(-position, wait, **kwargs)

	@property
	def position(self):
		return -super().position

diff_xv2_r = ReversedEpicsMotor('XF:11IDB-ES{Dif-Ax:XV2}Mtr', name='diff_xv2_r')

# Alias motors
sam_tth = diff_thh
