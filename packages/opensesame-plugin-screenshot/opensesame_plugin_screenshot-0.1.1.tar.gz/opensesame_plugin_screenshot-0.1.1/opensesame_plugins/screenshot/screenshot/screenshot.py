"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
from pathlib import Path
import os


class Screenshot(Item):

    def reset(self):
        self.var.verbose = 'no'
        self.var.filename_screenshot = ''

    def prepare(self):
        super().prepare()
        self.verbose = self.var.verbose

        if self.var.canvas_backend != 'psycho':
            raise OSException('Screenshot plugin only supports PsychoPy as backend')

        self.experiment_path = Path(os.path.normpath(os.path.dirname(self.var.logfile)))
        self.path = self.experiment_path / 'screenshots' / ('subject-' + str(self.var.subject_nr))
        Path(self.path).mkdir(parents=True, exist_ok=True)

    def run(self):
        self.set_item_onset()
        fname =  self.path / self.var.filename_screenshot
        self.experiment.window.getMovieFrame()
        self.experiment.window.saveMovieFrames(fname)
        self._show_message('Screenshot saved to: %s' % fname)

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtScreenshot(Screenshot, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        Screenshot.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
