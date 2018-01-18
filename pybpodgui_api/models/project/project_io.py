 # !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import glob
import hashlib, pybpodgui_api
from pybpodgui_api.utils.send2trash_wrapper import send2trash
from sca.formats import json
from sca.storage.repository import Repository

from pybpodgui_api.models.project.project_base import ProjectBase

from pybpodgui_api.exceptions.api_error import APIError

logger = logging.getLogger(__name__)


class ProjectIO(ProjectBase):

    def __init__(self):
        super(ProjectIO, self).__init__()

        self.repository = None

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def load(self, project_path):
        """
        Load project from a folder.

        :ivar str project_path: Full path of the project to load.
        """
        self.repository = repository = Repository(project_path).open()

        print()
        repository.pprint()
        print()

        self.uuid4= repository.uuid4 if repository.uuid4 else self.uuid4
        self.name = repository.get('name', None)
        self.path = repository.path
        
        logger.debug("==== LOAD TASKS ====")

        for infolder, path in self.__list_all_tasks_in_folder(project_path):
            task = self.create_task()
            task.load(path, {})

        logger.debug("==== LOAD BOARDS ====")

        # load boards
        for repo in repository.find('boards').list():
            board = self.create_board()
            board.load(repo)

        logger.debug("==== LOAD SUBJECTS ====")

        # load subjectgs
        for repo in repository.find('subjects').list():
            subject = self.create_subject()
            subject.load(repo)

        logger.debug("==== LOAD EXPERIMENTS ====")

        # load experiments
        for repo in repository.find('experiments').list():
            experiment = self.create_experiment()
            experiment.load(repo)
        
        logger.debug("==== LOAD FINNISHED ====")

        
        self.data_hash = self.__generate_project_hash()








    def save(self, project_path):
        """
        Save project data on file
        :param str project_path: path to project
        :return: project data saved on settings file
        """
        logger.debug("saving project path: %s",  project_path)
        logger.debug("current project name: %s", self.name)
        logger.debug("current project path: %s", self.path)

        if not self.path and os.path.exists(project_path):
            raise FileExistsError("Project folder already exists")

        # Check if we are updating a repository previously loaded or creating a new one.
        if self.repository:

            if project_path==self.repository.path:
                # If we are saving to the same folder,
                # then we are going to do a repository update.
                repository = self.repository
            else:
                # If we are saving the repository to a diferent path,
                # then we are going to do a "save as".
                repository = Repository(project_path)
        else:
            repository = Repository(project_path)

        self.path = repository.path



        ########### SAVE THE TASKS ###########
        for task in self.tasks:
            task_repo = repository.sub_repository('tasks', task.name, uuid4=task.uuid4)
            task.save(task_repo)

        """
        # remove from the tasks directory the unused tasks files
        tasks_paths = [task.path for task in self.tasks]
        for infolder, path in self.__list_all_tasks_in_folder(project_path):
            if path not in tasks_paths:
                logger.debug("Sending file [{0}] to trash".format(path))
                if infolder:
                    send2trash(os.path.dirname(path))
                else:
                    send2trash(path)
        """

        
        ########### SAVE THE BOARDS ###########
        boards_repo = repository.find('boards')
        for board in self.boards:
            board.save( 
                repository.sub_repository('boards', board.name, uuid4=board.uuid4)
            )

        #self.__clean_boards_path(project_path)

        ########### SAVE THE EXPERIMENTS ############
        for experiment in self.experiments:
            experiment.save(repository.sub_repository('experiments', experiment.name, uuid4=experiment.uuid4))

        #self.__clean_experiments_path(project_path)

        ########### SAVE THE SUBJECTS ###############
        for subject in self.subjects:
            subject.save(repository.sub_repository('subjects', subject.name, uuid4=subject.uuid4))

        #self.__clean_subjects_path(project_path)

        ########### SAVE THE PROJECT ############

        # create root nodes
        repository.uuid4    = self.uuid4
        repository.software = 'PyBpod GUI API v'+str(pybpodgui_api.__version__)
        repository.def_url  = 'http://pybpod.readthedocs.org'
        repository.def_text = 'This file contains information about a PyBpod project.'
        repository['name']  = self.name

        repository.save()   # mark the repository to be saved
        
        repository.pprint()

        return repository









    def is_saved(self):
        """
        Verifies if project has changes by doing a recursive checksum on all entities

        :rtype: bool
        """
        if not self.path:
            return False

        current_hash = self.__generate_project_hash()

        if self.data_hash != current_hash:
            logger.warning("Different project data hashes:\n%s\n%s", self.data_hash, current_hash)
            return False

        return True

    def collect_data(self, data):
        """
        Collect the data of the project. This function is used to calculate the checksum of the project and verify if it was updated.

        :rtype: dict
        """
        data.update({'name': self.name})
        data.update({'experiments': []})
        data.update({'boards': []})

        for board in self.boards:
            data['boards'].append(board.collect_data({}))

        for experiment in self.experiments:
            data['experiments'].append(experiment.collect_data({}))

        logger.debug("Project data: %s", data)

        return data

    def __save_project_hash(self):
        self.data_hash = self.__generate_project_hash()
        logger.debug("Project data hash: %s", self.data_hash)

    def __generate_project_hash(self):
        return hashlib.sha256(
            json.dumps(self.collect_data(data={}), sort_keys=True).encode('utf-8')).hexdigest()

    

    ##########################################################################
    ####### AUXILIAR FUNCTIONS ###############################################
    ##########################################################################


    def __clean_experiments_path(self, project_path):
        """
        Remove from the experiments directory the unused experiment files
        """
        experiments_paths = [experiment.path for experiment in self.experiments]
        for path in self.__list_all_experiments_in_folder(project_path):
            if path not in experiments_paths:
                logger.debug("Sending directory [{0}] to trash".format(path))
                send2trash(path)

    def __clean_subjects_path(self, project_path):
        """
        Remove from the experiments directory the unused experiment files
        """
        subjects_paths = [subject.path for subject in self.subjects]
        for path in self.__list_all_subjects_in_folder(project_path):
            if path not in subjects_paths:
                logger.debug("Sending directory [{0}] to trash".format(path))
                send2trash(path)

    def __clean_boards_path(self, project_path):
        """
        Remove from the boards directory the unused boards files
        """
        boards_paths = [board.path for board in self.boards]
        for path in self.__list_all_boards_in_folder(project_path):
            if path not in boards_paths:
                logger.debug("Sending folder [{0}] to trash".format(path))
                send2trash(path)

    def __generate_data_hash(self, data):
        data_hash = hashlib.sha256(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
        logger.debug("Experiment data hash: %s", data_hash)
        return data_hash

    def __list_all_experiments_in_folder(self, project_path):
        search_4_dirs_path = os.path.join(project_path, 'experiments')
        if not os.path.exists(search_4_dirs_path): return []
        return sorted([os.path.join(search_4_dirs_path, d) for d in os.listdir(search_4_dirs_path) if
                       os.path.isdir(os.path.join(search_4_dirs_path, d))])

    def __list_all_subjects_in_folder(self, project_path):
        search_4_dirs_path = os.path.join(project_path, 'subjects')
        if not os.path.exists(search_4_dirs_path): return []
        return sorted([os.path.join(search_4_dirs_path, d) for d in os.listdir(search_4_dirs_path) if
                       os.path.isdir(os.path.join(search_4_dirs_path, d))])

    def __list_all_tasks_in_folder(self, project_path):
        path = os.path.join(project_path, 'tasks')
        if not os.path.exists(path): return []
        
        tasksfiles   =  [(False, os.path.join(path, d)) for d in os.listdir(path) if os.path.isfile(os.path.join(path,d)) and d.lower().endswith('.py')]
        tasksfiles   += [(True,  os.path.join(path, d, d+'.py')) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d)) ]
        return sorted(tasksfiles)

    def __list_all_boards_in_folder(self, project_path):
        search_4_dirs_path = os.path.join(project_path, 'boards')
        if not os.path.exists(search_4_dirs_path): return []
        return sorted([os.path.join(search_4_dirs_path, d) for d in os.listdir(search_4_dirs_path) if
                       os.path.isdir(os.path.join(search_4_dirs_path, d))])
