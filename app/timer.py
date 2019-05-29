from app.functions import *


class Timer:
    started = False
    start_time = now()
    mark = now()
    cycles = 0
    distribution = {'early': 0, 'late': 0, 'on_target': 0}
    tcycle = 0
    past_15 = []

    def __init__(self, app, andon):
        self.app = app
        self.andon = andon

    def reset_all_variables(self):
        """ upon reset, all necessary variables and labels are reset to original """
        self.started = False
        self.cycles = 0
        self.distribution = {'early': 0, 'late': 0, 'on_target': 0}
        self.past_15 = []
        self.andon.reset()

        for label in ['early', 'late', 'on_target']:
            self.app.setLabel(label, label)

        self.app.changeOptionBox('past_10', ['previous cycles'])

    def update(self):
        """ all constantly updating gui labels should be updated from here, to keep the main count function clean """
        self.screen_color()
        self.ahead()
        self.app.setLabel('tCycle', countdown_format(self.tcycle))

    def start(self):
        """ the start button calls this function """
        if self.started:
            self.app.setButton('Start', 'Start')
            self.app.setButtonBg('Start', 'light grey')
            self.reset_all_variables()

        else:
            self.started = True
            self.mark = now()
            self.start_time = now()
            self.app.setTabbedFrameSelectedTab('Tabs', 'Run')
            self.app.setButton('Start', 'Reset')
            self.app.setButtonBg('Start', 'red')
            time_label = '{} Cycle Time\n{} PCT * {} Parts'.format(countdown_format(self.sequence_time()),
                                                                   countdown_format(int(self.app.getLabel('PCT'))),
                                                                   self.app.getLabel('partsper'))
            self.app.setLabel('sequence_time', time_label)

    def cycle(self):
        """ called when the user presses the pedal each cycle """
        if self.started and self.tcycle < self.sequence_time() - 2:
            current = self.get_current()
            cycle_time = self.sequence_time() - self.tcycle
            self.distribution[current] += 1
            self.cycles += 1
            self.past_15.append('{}; {}'.format(countdown_format(cycle_time), current))
            self.past_15 = self.past_15[1:] if len(self.past_15) > 15 else self.past_15
            self.app.changeOptionBox('past_10', self.past_15)
            self.app.setOptionBox('past_10', self.past_15[-1])
            self.mark = now()
            self.app.setLabel(current, current + ': {}'.format(self.distribution[current]))

    def screen_color(self):
        """ changes the timer color based off current cycle status ( self.get_current() ) """
        current = self.get_current()
        color = self.app.getLabelBg('tCycle')
        new_color = 'light grey' if current == 'early' else 'yellow' if current == 'on_target' else 'red'
        if color != new_color:
            self.app.setLabelBg('tCycle', new_color)

    def ahead(self):
        """ updates the ahead label to show current state """
        expected = int((now() - self.start_time).total_seconds() // self.sequence_time())
        ahead = self.cycles - expected
        label = "Ahead {} ({}/{})" if ahead >= 0 else "Behind {} ({}/{})"
        ahead *= -1 if ahead < 0 else 1
        self.app.setLabel('ahead', label.format(ahead, self.cycles, expected))

    def sequence_time(self):
        """ returns PCT * Partsper, the expected sequence cycle time """
        return int(self.app.getLabel('PCT')) * int(self.app.getLabel('partsper'))

    def window(self):
        """ returns the acceptable window for "on time" delivery """
        return int(self.app.getLabel('partsper'))  # currently +/- 1sec/part

    def get_current(self):
        """ returns whether the current cycle is early, on_target, or late (as str) """
        current_time = self.tcycle
        if current_time > self.window():
            return 'early'
        elif -self.window() <= current_time <= self.window():
            return 'on_target'
        else:
            return 'late'

