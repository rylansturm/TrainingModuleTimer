"""
The app is passed to the 'layout' function which creates all labels, buttons, tabs, etc.

Current app layout is:

Tabs:
    1.  Main
            the current cycle time, as well as live metrics and buttons for the andon system
    2.  Setup
            two keypads for adjusting the PCT and Partsper variables
"""

from app.functions import *
import os

raspi = os.sys.platform == 'linux'  # boolean to prevent calling raspi specific functionality when testing
title = 'Timer'  # app title - functionally arbitrary
size = (800, 480)  # window size in pixels (ignored if raspi)
bg = 'light grey'  # main background color
font = 16  # universal font, unless specified below
font_large = 'arial 60'  # |
font_bold = 'arial 16 bold'  # |
font_tCycle = 'arial 148'  # |
font_glance = 'arial 24 bold'  # |


def layout(app, andon, pct, partsper, timer):
    """ a blank appJar.gui object is passed through this function to generate formatting, labels, buttons, etc. """

    app.setFont(font)
    app.setTitle(title)
    app.setSize('fullscreen' if raspi else size)

    """ 
    It's pretty easy to follow the layout of the app by following the indentation of the "with" statements 

    | this level has the separate windows (tabbedFrame and subWindow)
    |
        | this level has the separate tabs ("Main", "Setup", "Schedule" as documented above)
        |
            | this level and deeper has the labels, frames, buttons that rest in the frames
            |
    """

    with app.tabbedFrame('Tabs'):
        """ this is the frame the whole gui sits in """

        # Setup Tab - Where you set PCT and Parts per Cycle
        with app.tab('Setup'):
            app.setBg(bg)

            with app.labelFrame('Planned Cycle Time', row=0, column=0):
                app.setLabelFrameAnchor('Planned Cycle Time', 'n')
                app.getLabelFrameWidget('Planned Cycle Time').config(font=font_bold)
                app.setSticky('news')
                app.addLabel('PCT', pct.planned_cycle_time, row=0, column=0)
                app.getLabelWidget('PCT').config(font=font_large)

                with app.frame('PCT_entry', row=1, column=0):
                    app.setSticky('news')
                    app.addEntry('new_pct', colspan=3)
                    app.setEntryAlign('new_pct', 'center')
                    for button in range(1, 10):
                        name = '%s_PCT' % button
                        app.addButton(name, pct.set_pct, row=((button - 1) // 3) + 2, column=(button + 2) % 3)
                        app.setButton(name, button)
                        app.setButtonWidth(name, 1)
                    col = 0
                    for button in ['Back', '0', 'OK']:
                        name = button + '_PCT'
                        app.addButton(name, pct.set_pct, row=5, column=col)
                        col += 1
                        app.setButton(name, button)
                        app.setButtonWidth(name, 1)

            with app.labelFrame('Parts Per Cycle', row=0, column=1):
                app.setLabelFrameAnchor('Parts Per Cycle', 'n')
                app.getLabelFrameWidget('Parts Per Cycle').config(font=font_bold)
                app.setSticky('news')
                app.addLabel('partsper', partsper.partsper, row=0, column=0)
                app.getLabelWidget('partsper').config(font=font_large)

                with app.frame('partsper_entry', row=1, column=0):
                    app.setSticky('news')
                    app.addEntry('new_partsper', colspan=3)
                    app.setEntryAlign('new_partsper', 'center')
                    for button in range(1, 10):
                        name = '%s_partsper' % button
                        app.addButton(name, partsper.set_partsper, row=((button - 1) // 3) + 1, column=(button + 2) % 3)
                        app.setButton(name, button)
                        app.setButtonWidth(name, 1)
                    col = 0
                    for button in ['Back', '0', 'OK']:
                        name = button + '_partsper'
                        app.addButton(name, partsper.set_partsper, row=4, column=col)
                        col += 1
                        app.setButton(name, button)
                        app.setButtonWidth(name, 1)
            app.addButton('Start', timer.start, colspan=2)

        # Main Tab - Where the timer and metrics are visible
        with app.tab('Run'):
            app.setBg(bg)

            with app.frame('tCycle_frame', row=0, column=0):
                app.setFrameWidth('tCycle_frame', 5)
                app.addLabel('tCycle', '0', row=0, column=0)
                app.setLabelSticky('tCycle', 'news')
                app.getLabelWidget('tCycle').config(font=font_tCycle)

            with app.frame('totals', row=1, column=0):

                with app.frame('glance', row=0, colspan=4):
                    column = 0
                    for label in ['ahead', 'sequence_time']:
                        app.addLabel(label, row=0, column=column)
                        app.getLabelWidget(label).config(font=font_glance)
                        app.setLabelRelief(label, 'ridge')
                        column += 1

                column = 0
                for label in ['early', 'late', 'on_target']:
                    app.addLabel(label, row=1, column=column)
                    app.setLabelRelief(label, 'ridge')
                    app.getLabelWidget(label).config(font=font_bold)
                    column += 1
                app.addOptionBox('past_10', ['previous cycles'], row=1, column=3)

            with app.frame('Andons', row=0, column=1, rowspan=2):
                app.setFrameWidth('Andons', 2)
                app.addButton('Andon', andon.andon)
                app.setButtonBg('Andon', '#AAAAAA')
                app.getButtonWidget('Andon').config(font=font_bold)
                app.setButtonHeight('Andon', 10)
                app.setButtonWidth('Andon', 1)
                app.addButton('Respond', andon.andon)
                app.setButtonHeight('Respond', 1)
                app.setButtonWidth('Respond', 1)
                app.addLabel('andons', andon.andons)
                app.getLabelWidget('andons').config(font=font_bold)

    return app
