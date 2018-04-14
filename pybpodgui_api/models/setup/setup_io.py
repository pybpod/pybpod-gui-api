# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os, glob, hashlib
import pybpodgui_api
from pybpodgui_api.utils.send2trash_wrapper import send2trash
from pybpodgui_api.models.setup.setup_base import SetupBase

from sca.formats import json

logger = logging.getLogger(__name__)


class SetupBaseIO(SetupBase):


    def __init__(self, experiment):
        super(SetupBaseIO, self).__init__(experiment)

        # repository that will manage the project files
        self.repository = None


    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'board': self.board.name if self.board else None})
        self.board_task.collect_data(data)
        return data


    def save(self, parent_repository):
        """
        Save setup data on filesystem.

        :ivar str parent_path: Experiment path.  
        :return: Dictionary containing the setup info to save.  
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping setup without name")
        else:
            # if the project was loaded then it will reuse the repository otherwise create a new repository ################################
            repository = self.repository = self.repository if self.repository else parent_repository.sub_repository('setups', self.name, uuid4=self.uuid4)
            ################################################################################################################################

            # save sessions
            for session in self.sessions: session.save(repository)

            repository.uuid4        = self.uuid4
            repository.software     = 'PyBpod GUI API v'+str(pybpodgui_api.__version__)
            repository.def_url      = 'http://pybpod.readthedocs.org'
            repository.def_text     = 'This file contains the configuration of a setup from PyBpod system.'
            repository.name         = self.name
            
            repository['board']     = self.board.name if self.board else None
            repository['task']      = self.task.name if self.task else None
            repository['subjects']  = [subject.name for subject in self.subjects]
            repository['detached']  = self.detached
            repository.update( self.board_task.save() ) # collect board_task data
            
            if self.board:                repository.add_external_ref(self.board.uuid4)
            for subject in self.subjects: repository.add_external_ref(subject.uuid4)

            repository.commit()
            
            return repository

    def load(self, repository):
        """
        Load setup data from filesystem

        :ivar str setup_path: Path of the setup
        :ivar dict data: data object that contains all setup info
        """
        self.repository = repository

        self.name = repository.name

        self.uuid4 = repository.uuid4 if repository.uuid4 else self.uuid4
        self.board = repository.get('board', None)
        self.task  = repository.get('task', None)

        if self.board: repository.add_external_ref(self.board.uuid4)
        if self.task:  repository.add_external_ref(self.task.uuid4)
        
        self.detached = repository.get('detached', False)
        self.board_task.load(repository)
        
        for subject_name in repository.get('subjects', []):
            self += self.project.find_subject(subject_name)
        

        # load experiments
        sessions_repo = repository.find('sessions')
        if sessions_repo is not None:
            for repo in sessions_repo.list():
                session = self.create_session()
                session.load(repo)

        self._sessions = sorted(self.sessions, key=lambda x: x.started, reverse=True)