# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os, uuid
from pybpodgui_api.utils.send2trash_wrapper import send2trash

logger = logging.getLogger(__name__)

class OtherTaskFileBase(object):
    """ Represents a state machine """

    def __init__(self, task=None ):
        """
        :ivar Project project: Project to which the Task belongs to.
        """
        self._name    = ''
        self.uuid4    = uuid.uuid4()
        self.task     = task
        self.task    += self
        self.filepath = None

    @property
    def filepath(self): return self._filepath

    @filepath.setter
    def filepath(self, value): 
        self._filepath = value

        if value is None:
            self.name = 'Other task file {0}'.format( len(self.task.otherfiles) ) if self.task else None
        else:
            self.name = os.path.basename(value)


    @property
    def name(self): return self._name

    @name.setter
    def name(self, value): self._name = value