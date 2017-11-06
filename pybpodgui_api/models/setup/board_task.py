# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from pybpodgui_api.exceptions.invalid_task import InvalidTaskError
from pybpodgui_api.models.setup.task_variable import TaskVariable

logger = logging.getLogger(__name__)


class BoardTask(object):
    """
    Represents the association between one board and one task
    """

    def __init__(self, setup):
        """
        :ivar Setup setup: Setup to which the BoardTask belongs to
        """
        self.setup = setup
        self.board = None
        self.task  = None
        self.variables = []
        
    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def board(self):
        """
        Get and set the board

        :rtype: Board
        """
        return self._board

    @board.setter
    def board(self, value): self._board = value

    @property
    def task(self):
        """
        Get and set the Task

        :rtype: Task
        """
        return self._task

    @task.setter
    def task(self, value): self._task = value

    @property
    def variables(self):
        """
        Get and set list of variables

        :rtype: list(TaskVariable)
        """
        return self._variables

    @variables.setter
    def variables(self, value): self._variables = value

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def create_variable(self, name=None, value=None, datatype='string'):
        """
        Create a variable

        :rtype: TaskVariable
        """
        return TaskVariable(self, name, value, datatype)

    def collect_data(self, data):
        data.update({'variables': [var.collect_data({}) for var in self.variables]})
        return data

    def save(self, setup_path):
        """
        Save board task data on filesystem.

        :ivar str setup_path: Setup path.  
        :return: Dictionary containing the board task info to save.  
        :rtype: dict
        """
        return {'variables': [var.save(setup_path) for var in self.variables]}

    def load(self, setup_path, data):
        """
        Load setup data from filesystem

        :ivar str setup_path: Path of the setup
        :ivar dict data: data object that contains all setup info
        """
        for data in data.get('variables', []):
            var = self.create_variable()
            var.load(setup_path, data)          


    def __unicode__(self):
        return "Board : {board} | Task: {task}".format(board=str(self.board), task=str(self.task))

    def __str__(self):
        return self.__unicode__()

    def __add__(self, other):
        if isinstance(other, TaskVariable): self.variables.append(other)
        return self
