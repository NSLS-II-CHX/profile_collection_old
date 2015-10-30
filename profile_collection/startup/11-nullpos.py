import time as ttime

class NullStatus(object):
    def __init__(self):
        self.done = True


class NullPositioner(object):

    def __init__(self, name=None):
        self.name = name
        self._name=name
        self.pvname = ['pain']
        self.report = {'pv': 'pain'}

        self.position = 0

    def move_next(self, *args, **kwargs):
        next(self.traj_iter)
        st = NullStatus()
        print(st.done)
        st.done = True
        return None, st

    def move(self, position, **kwargs):
        return NullStatus()

    @property
    def timestamp(self):
        return [ttime.time()]

    def set_trajectory(self, traj):
        self.traj = traj
        self.traj_iter = iter(traj)

    def check_value(self, *args, **kwargs):
        return True

    def describe(self):
        return {}

    def read(self):
        return {}

nullmtr = NullPositioner(name='nullmtr')
