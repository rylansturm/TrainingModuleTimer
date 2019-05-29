from app import create_app
from app.layout import layout
from app.functions import *


class Timer:
    def __init__(self):
        new_timer_object = create_app()
        app = new_timer_object['app']

        self.andon = new_timer_object['andon']
        self.pct = new_timer_object['pct']
        self.partsper = new_timer_object['partsper']
        self.timer = new_timer_object['timer']

        self.app = layout(app, self.andon, self.pct, self.partsper, self.timer)
        self.app.registerEvent(self.count)
        self.app.setPollTime(50)
        self.app.bindKey('1', self.timer.cycle)

    def count(self):
        """ runs repeatedly while gui is running """

        timer = self.timer
        cycle = (now() - timer.mark).total_seconds()
        timer.tcycle = int(timer.sequence_time() - (int(cycle) if timer.started else 0))
        timer.update()


if __name__ == '__main__':
    App = Timer()
    App.app.go()
