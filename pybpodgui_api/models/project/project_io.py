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

        self.repository = None # repository which will manage project files 
        self.data_hash  = None

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def load(self, project_path):
        """
        Load project from a folder.

        :ivar str project_path: Full path of the project to load.
        """
        self.repository = Repository(project_path).open()

        #print()
        #self.repository.pprint()
        #print()

        self.uuid4= self.repository.uuid4 if self.repository.uuid4 else self.uuid4
        self.name = self.repository.name
        self.path = self.repository.path
        
        logger.debug("==== LOAD TASKS ====")

        tasks_repo = self.repository.find('tasks')
        if tasks_repo is not None:
            for repo in tasks_repo.list():
                task = self.create_task()
                task.load(repo)

        logger.debug("==== LOAD BOARDS ====")

        # load boards
        boards_repo = self.repository.find('boards')
        if boards_repo is not None:
            for repo in boards_repo.list():
                board = self.create_board()
                board.load(repo)

        logger.debug("==== LOAD SUBJECTS ====")

        # load subjects
        subjects_repo = self.repository.find('subjects')
        if subjects_repo is not None:
            for repo in subjects_repo.list():
                subject = self.create_subject()
                subject.load(repo)

        logger.debug("==== LOAD EXPERIMENTS ====")

        # load experiments
        experiments_repo = self.repository.find('experiments')
        if experiments_repo is not None:
            for repo in experiments_repo.list():
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


        #if not self.path and os.path.exists(project_path):
        #    raise FileExistsError("Project folder already exists")

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
        for task in self.tasks:   task.save(repository)

        ########### SAVE THE BOARDS ###########
        for board in self.boards: board.save(repository)

        ########### SAVE THE EXPERIMENTS ############
        for experiment in self.experiments: experiment.save(repository)

        ########### SAVE THE SUBJECTS ###############
        for subject in self.subjects: subject.save(repository)

        ########### SAVE THE PROJECT ############

         # create root nodes
        repository.uuid4    = self.uuid4
        repository.software = 'PyBpod GUI API v'+str(pybpodgui_api.__version__)
        repository.def_url  = 'http://pybpod.readthedocs.org'
        repository.def_text = 'This file contains information about a PyBpod project.'
        repository.name     = self.name

        repository.commit()
        

        """
        tasks_repo = self.repository.find('tasks')
        print('tasks', [c.name for c in tasks_repo.children])
        boards_repo = self.repository.find('boards')
        print('boards', [c.name for c in boards_repo.children])
        subjects_repo = self.repository.find('subjects')
        print('subjects', [c.name for c in subjects_repo.children])
        experiments_repo = self.repository.find('experiments')
        print('experiments', [c.name for c in experiments_repo.children])
        
        for arep in repository.find('experiments').list():
            for brep in arep.find('setups').list():
                crep = brep.find('sessions')
                print('session','|', brep.name,'|', crep.name,'|', [c.name for c in crep.children])
        #repository.close_save_session()
        """
        #repository.pprint()

        self.data_hash = self.__generate_project_hash()

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