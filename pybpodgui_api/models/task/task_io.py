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

        # repository that will manage the project files
        self.repository = None


    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def save(self, parent_repository):
        """
        Save setup data on filesystem.

        :ivar str project_path: Project path.  
        :ivar dict data: Dictionary where to save the data to.
        :return: Dictionary containing the task info to save.  
        :rtype: dict
        """

        # if the project was loaded then it will reuse the repository otherwise create a new repository ################################
        repository = self.repository = self.repository if self.repository else parent_repository.sub_repository('tasks', self.name, uuid4=self.uuid4, fileformat='py')
        ################################################################################################################################

        #force the creation of the file
        self.filepath = self.make_emptyfile() if not self.filepath else self.filepath

        repository.path                 = self.path
        repository['name']              = self.name
        repository['trigger-softcodes'] = self.trigger_softcodes
        repository['commands']          = [cmd.save() for cmd in self.commands]
        repository.name                 = self.name
        
        repository.commit()

        


    def load(self, repository):
        """
        Load setup data from filesystem

        :ivar str task_path: Path of the task
        :ivar dict data: data object that contains all task info
        """
        self.repository = repository

        self.name     = repository.name
        self.uuid4    = repository.uuid4 if repository.uuid4 else self.uuid4
        self.filepath = os.path.join(self.path, self.name+'.py')
        self.trigger_softcodes = repository.get('trigger-softcodes', None)

        for data in repository.get('commands', []):
            cmd = getattr(self, data['type'])()
            cmd.load(data)