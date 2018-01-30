# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os, json, glob, hashlib
from pybpodgui_api.utils.send2trash_wrapper import send2trash
from pybpodgui_api.models.setup.setup_base import SetupBase

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

            data2save = {}
            data2save.update({'name': self.name})
            data2save.update({'board': self.board.name if self.board else None})
            data2save.update({'subjects': [subject.name for subject in self.subjects]})
            data2save.update(board_task_data)

            self.__clean_sessions_path(setup_path)

            self.__save_on_file(data2save, dest_path=setup_path, filename='setup-settings.json')

            self.path = setup_path

            return data2save

    def load(self, setup_path, data):
        """
        Load setup data from filesystem

        :ivar str setup_path: Path of the setup
        :ivar dict data: data object that contains all setup info
        """
        settings_path = os.path.join(setup_path, 'setup-settings.json')
        self.path = setup_path

        with open(settings_path, 'r') as output_file:
            data = json.load(output_file)
            self.name  = data['name']
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
        search_4_files_path = os.path.join(setup_path, '*.txt')
        return sorted(glob.glob(search_4_files_path))
