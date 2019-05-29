class Andon:
    """ andons -> int; The number of times an operator has signaled an abnormality
        only two buttons interact with the andon system, 'Andon' and 'Respond' """
    andons = 0
    responded = 0  # used to show how many andons the team leader has already responded to

    def __init__(self, app):
        self.app = app

    def andon(self, btn):
        """ handles the two andon buttons ['Andon', 'Respond'] """
        if btn == 'Andon':  # operator signals andon, changing LED to red
            self.andons += 1
            self.app.setButtonBg('Andon', '#DD3333')
        if btn == 'Respond':  # team leader responds to andon and resets andon LED
            self.responded = self.andons
            self.app.setButtonBg('Andon', '#AAAAAA')
        self.app.setLabel('andons', self.get_andons())

    def get_andons(self):
        """ returns the label shown under the andon buttons """
        andons, responded = self.andons, self.responded
        if responded != andons:
            return '{} + {}'.format(responded, andons - responded)
        else:
            return andons

    def reset(self):
        self.andons, self.responded = 0, 0
        self.andon('Respond')
