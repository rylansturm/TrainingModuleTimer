class Partsper:
    """partsper -> int; the number of parts this sequence produces in one cycle"""
    partsper = 1

    def __init__(self, app):
        self.app = app

    def set_partsper(self, btn):
        """ handles button pushes relative to partsper adjustments """
        new = self.app.getEntry('new_partsper')
        if btn == 'OK_partsper':
            if new != '':
                self.partsper = int(new)
                self.app.setLabel('partsper', self.partsper)
                self.app.setEntry('new_partsper', '')
        elif btn == 'Back_partsper':
            self.app.setEntry('new_partsper', new[0:-1])
        else:
            self.app.setEntry('new_partsper', self.validate(new + btn[0]))

    @staticmethod
    def validate(new):
        """ makes sure invalid numbers can't be set to partsper """
        if 0 < int(new) <= 72:
            return new
        else:
            return new[0:-1]
