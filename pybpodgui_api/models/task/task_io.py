# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os
from pybpodgui_api.models.task.task_base import TaskBase

logger = logging.getLogger(__name__)


class TaskIO(TaskBase):
    """
    Task I/O operations
    """

    def __init__(self, project=None):
        super(TaskIO, self).__init__(project)

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def save(self, repository):
        """
        Save setup data on filesystem.

        :ivar str project_path: Project path.  
        :ivar dict data: Dictionary where to save the data to.
        :return: Dictionary containing the task info to save.  
        :rtype: dict
        """
        new_task_path = os.path.join(repository.path, self.name) + '.py'

        if self.path != new_task_path:
            # if the task file is not in the project file, it makes a copy to the project folder
            code_txt = self.code if self.path else ''
            self.path = new_task_path
            self.code = code_txt

        repository.uuid4 = self.uuid4
        repository.save()


    def load(self, task_path, data):
        """
        Load setup data from filesystem

        :ivar str task_path: Path of the task
        :ivar dict data: data object that contains all task info
        """
        self.name = os.path.splitext(os.path.basename(task_path))[0]
        self.path = task_path
