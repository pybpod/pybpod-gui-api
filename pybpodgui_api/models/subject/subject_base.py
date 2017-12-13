# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os, uuid
from pybpodgui_api.models.setup.board_task import BoardTask
from pybpodgui_api.models.session import Session

logger = logging.getLogger(__name__)


class SubjectBase(object):

    def __init__(self, project):
        self._path      = None

        self.uuid4      = uuid.uuid4()
        
        self.name       = 'Untitled subject {0}'.format(len(project.subjects))
        self.project    = project

        self.project    += self
        
    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def name(self):
        """
        Get and set setup name

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):      self._name = value

    @property
    def project(self):
        """
        Get and set project

        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, value):   self._project = value

    @property
    def path(self):
        """
        Get and set the path

        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, value):      self._path = value

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def remove(self):
        """
        Remove the subject from the project
        """
        pass

    def __unicode__(self):  return self.name
    def __str__(self):      return self.__unicode__()


