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

            # check if the tasks path exists, if not create it
            tasks_path = os.path.join(self.project.path, 'tasks')
            if not os.path.exists(tasks_path):  os.makedirs(tasks_path)

            # check if the task path exists, if not create it
            task_folder = os.path.join(tasks_path, self.name)
            if not os.path.exists(task_folder): os.makedirs(task_folder)
            
            open(self.filepath, "w").close()
            
        repository.add_file( self.filepath , self.name+'.py')
        
        repository['name'] = self.name

        
        repository['other-files'] = {}
        for otherfile in self.otherfiles:
            repository['other-files'][otherfile.name] = {}
            otherfile.save(repository)

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
        
        otherfiles_data = repository.get('other-files', {})

        for filepath in os.listdir(self.path):
            full_filepath = os.path.join(self.path,filepath)

            if self.filepath == full_filepath: continue

            settings_file = os.path.join(repository.path, repository.name+'.json')
            if settings_file == full_filepath: continue

            if os.path.isfile(full_filepath):
                o = self.create_otherfile()
                o.filepath = full_filepath
                
                o.load(repository)
