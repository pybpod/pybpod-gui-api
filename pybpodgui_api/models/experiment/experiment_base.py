# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from pybpodgui_api.models.setup import Setup

logger = logging.getLogger(__name__)


class ExperimentBase(object):
    """
    Experiment entity details.
    Each experiment should have a name, a list of setups, a project belonging to, a path and a task.
    """

    def __init__(self, project):
        """
        :ivar Project project: project object reference
        """
        self.name = 'Untitled experiment {0}'.format(len(project.experiments))
        self._setups = []
        self.project = project
        self.path = None
        self.task = None

        self.project += self

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def name(self):
        """
        Get and set the experiment name

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def task(self):
        """
        Get and set the experiment task

        :rtype: Task
        """
        return self._task

    @task.setter
    def task(self, value):
        if isinstance(value, str): value = self.project.find_task(value)
        self._task = value
        for setup in self.setups:
            setup.task = value

    @property
    def project(self):
        """
        Get and set the experiment project

        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, value):
        self._project = value

    @property
    def setups(self):
        """
        Get the experiment setups

        :rtype: list(Setup)
        """
        return self._setups

    @property
    def path(self):
        """
        Get and set the experiment files path

        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def remove(self):
        """
        Remove experiment
         
        """
        pass

    def create_setup(self):
        """
        Create new instance of setup
        
        :rtype: Setup
        """
        return Setup(self)

    def __add__(self, obj):
        if isinstance(obj, Setup): self._setups.append(obj)
        return self

    def __sub__(self, obj):
        if isinstance(obj, Setup): self._setups.remove(obj)
        return self

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()