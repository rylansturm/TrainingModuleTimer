from app.functions import *


class PCT:
    """pct -> int; number of seconds planned for cycling each part through flow"""
    planned_cycle_time = 60

    def __init__(self, app):
        self.app = app

    def set_pct(self, btn):
        """ handles buttons related to PCT adjustment """
        new = self.app.getEntry('new_pct')
        if btn == 'OK_PCT':
            if new != '':
                self.planned_cycle_time = int(new)
                self.app.setLabel('PCT', self.planned_cycle_time)
                self.app.setEntry('new_pct', '')
                partsper = int(self.app.getLabel('partsper'))
                sequence_time = self.planned_cycle_time * partsper
                time_label = '{} Cycle Time\n{} PCT * {} Parts'.format(countdown_format(sequence_time),
                                                                       countdown_format(self.planned_cycle_time),
                                                                       partsper)
                self.app.setLabel('sequence_time', time_label)
        elif btn == 'Back_PCT':
            self.app.setEntry('new_pct', new[0:-1])
        else:
            self.app.setEntry('new_pct', self.validate(new + btn[0]))

    @staticmethod
    def validate(new):
        """ makes sure invalid numbers can't be set to pct """
        if 0 < int(new) <= 3600:
            return new
        else:
            return new[0:-1]
