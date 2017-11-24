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


    def save(self, parent_path):
        """
        Save setup data on filesystem.

        :ivar str parent_path: Experiment path.  
        :return: Dictionary containing the setup info to save.  
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping setup without name")
        else:
            setups_path = self.__generate_setups_path(experiment_path=parent_path)
            if not os.path.exists(setups_path):
                os.makedirs(setups_path)

            setup_path = self.__generate_setup_path(setups_path)
            if not os.path.exists(setup_path):
                os.makedirs(setup_path)

            # collect board_task data
            board_task_data = self.board_task.save(parent_path)

            # save sessions
            for session in self.sessions:
                session.save(setup_path)

            data2save = json.scadict({
                    'name':     self.name,
                    'board':    self.board.name if self.board else None,
                    'subjects': [subject.name for subject in self.subjects]
                },
                uuid4_id=self.uuid4,
                software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                def_url='http://pybpod.readthedocs.org',
                def_text='This file contains the configuration of a setup from PyBpod system.')

            data2save.update(board_task_data)

            self.__clean_sessions_path(setup_path)

            data2save.add_parent_ref(self.experiment.uuid4)
            if self.board: 
                data2save.add_external_ref(self.board.uuid4)
            for subject in self.subjects:
                data2save.add_external_ref(subject.uuid4)

            with open(os.path.join(setup_path, 'setup-settings.json'), 'w') as jsonfile:
                json.dump(data2save, jsonfile)
                
            self.path = setup_path

            return data2save

    def load(self, setup_path, data):
        """
        Load setup data from filesystem

        :ivar str setup_path: Path of the setup
        :ivar dict data: data object that contains all setup info
        """
        self.path = setup_path
        self.name = os.path.basename(setup_path)

        with open(os.path.join(setup_path, 'setup-settings.json'), 'r') as jsonfile:
            data       = json.load(jsonfile)
            self.uuid4 = data.uuid4 if data.uuid4 else self.uuid4
            self.board = data.get('board', None)
            for subject_name in data.get('subjects', []):
                self += self.project.find_subject(subject_name)
            self.board_task.load(setup_path, data)

        for filepath in self.__list_all_sessions_in_folder(setup_path):
            session = self.create_session()
            session.load(filepath, {})

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
