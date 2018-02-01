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

        #force the creation of the file
        if not self.filepath:
            self.filepath = os.path.join(self.path, self.name+'.py')
            self.code = ''
            
        repository.add_file( self.filepath , self.name+'.py')
        
        repository['name'] = self.name
        repository.save()

        self.name = repository.name

        if self.filepath:
            self.filepath = os.path.join(self.path, self.name+'.py')
        


    def load(self, repository):
        """
        Load setup data from filesystem

        :ivar str task_path: Path of the task
        :ivar dict data: data object that contains all task info
        """
        self.name   = repository.name
        self.uuid4  = repository.uuid4 if repository.uuid4 else self.uuid4
        self.filepath = os.path.join(self.path, self.name+'.py')
        