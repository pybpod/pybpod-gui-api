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

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'board': self.board.name if self.board else None})
        self.board_task.collect_data(data)
        return data


    def save(self, repository):
        """
        Save setup data on filesystem.

        :ivar str parent_path: Experiment path.  
        :return: Dictionary containing the setup info to save.  
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping setup without name")
        else:
            # save sessions
            for session in self.sessions:     
                rep = repository.sub_repository(
                    'sessions',
                    session.name, 
                    uuid4=session.uuid4,
                    fileformat='csv'
                )
                session.save(rep)

            repository.uuid4    = self.uuid4
            repository.software = 'PyBpod GUI API v'+str(pybpodgui_api.__version__)
            repository.def_url  = 'http://pybpod.readthedocs.org'
            repository.def_text = 'This file contains the configuration of a setup from PyBpod system.'
            repository['name']      = self.name
            repository['board']     = self.board.name if self.board else None
            repository['subjects']  = [subject.name for subject in self.subjects]

            
            # collect board_task data
            repository.update(self.board_task.save())

            #self.__clean_sessions_path(setup_path)

            repository.add_parent_ref(self.experiment.uuid4)
            if self.board: 
                repository.add_external_ref(self.board.uuid4)
            for subject in self.subjects:
                repository.add_external_ref(subject.uuid4)

            self.path = repository.save()

            return repository

    def load(self, repository):
        """
        Load setup data from filesystem

        :ivar str setup_path: Path of the setup
        :ivar dict data: data object that contains all setup info
        """
        self.path = repository.path
        self.name = repository.name

        self.uuid4 = repository.uuid4 if repository.uuid4 else self.uuid4
        self.board = repository.get('board', None)
        
        self.board_task.load(repository)
        
        for subject_name in repository.get('subjects', []):
            self += self.project.find_subject(subject_name)
        
        for repo in repository.find('sessions').list():
            session = self.create_session()
            session.load(repo)

        self._sessions = sorted(self.sessions, key=lambda x: x.started)

    def __save_on_file(self, data2save, dest_path, filename):
        """
        Dump data on file
        :param data2save:
        :param dest_path:
        :param filename:
        """
        settings_path = os.path.join(dest_path, filename)
        with open(settings_path, 'w') as output_file:
            json.dump(data2save, output_file, sort_keys=False, indent=4, separators=(',', ':'))

    def __clean_sessions_path(self, setup_path):
        """
        Remove from the sessions file the unused session files
        """
        sessions_paths = [session.path for session in self.sessions]
        for path in self.__list_all_sessions_in_folder(setup_path):
            if path not in sessions_paths:
                send2trash(path)

    def __generate_setups_path(self, experiment_path):
        return os.path.join(experiment_path, 'setups')

    def __generate_setup_path(self, setups_path):
        return os.path.join(setups_path, self.name)

    def __list_all_sessions_in_folder(self, setup_path):
        search_4_files_path = os.path.join(setup_path, '*.csv')
        return sorted(glob.glob(search_4_files_path))
