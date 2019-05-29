from app import andon, pct, partsper, timer
import sys
sys.path.insert(0, '/home/pi/TaktTimer/venv/Lib/site-packages')  # All dependencies are in virtual environment
from appJar import gui  # http://appjar.info  for documentation
#                       # this is the main library for creating the gui


def create_app():
    app = gui()
    andon_class = andon.Andon(app)
    pct_class = pct.PCT(app)
    partsper_class = partsper.Partsper(app)
    timer_class = timer.Timer(app, andon_class)
    return {'app': app,
            'andon': andon_class,
            'pct': pct_class,
            'partsper': partsper_class,
            'timer': timer_class
            }
