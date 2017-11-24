# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os, hashlib
import pybpodgui_api
from pybpodgui_api.utils.send2trash_wrapper import send2trash
from pybpodgui_api.models.experiment.experiment_base import ExperimentBase

from sca.formats import json

logger = logging.getLogger(__name__)


class ExperimentIO(ExperimentBase):
    """
    Save and Load actions for Experiment
    """

    def __init__(self, project):
        super(ExperimentIO, self).__init__(project)

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'task': self.task.name if self.task else None})
        data.update({'setups': []})

        for setup in self.setups:
            data['setups'].append(setup.collect_data({}))

        return data

    def save(self, parent_path):
        """
        Save experiment data on filesystem.

        :ivar dict parent_path: Project path.  
        :return: Dictionary containing the experiment info to save.  
        :rtype: dict
        """
        #generate the experiments folder if does not exists
        experiments_path = self.__generate_experiments_path(parent_path)
        if not os.path.exists(experiments_path):
            os.makedirs(experiments_path)

        #generate the experiment folder if does not exists
        experiment_path = self.__generate_experiment_path(experiments_path)
        if not os.path.exists(experiment_path):
            os.makedirs(experiment_path)

        # save setups
        for setup in self.setups:
            setup.save(parent_path=experiment_path)

        data2save = json.scadict({
                'name': self.name,
                'task': self.task.name if self.task else None
            },
            uuid4_id=self.uuid4,
            software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
            def_url ='http://pybpod.readthedocs.org',
            def_text='This file contains information about a PyBpod gui experiment.'
        )
        
        data2save.add_parent_ref(self.project.uuid4)
        if self.task: data2save.add_external_ref(self.task.uuid4)

        self.path = experiment_path

        self.__clean_setups_path(experiment_path)  # call only after update setups

        with open(os.path.join(experiment_path, 'experiment-settings.json'), 'w') as jsonfile:
            json.dump(data2save, jsonfile)
        
        return data2save


    def load(self, experiment_path, data):
        """
        Load experiment data from filesystem

        :ivar str experiment_path: Path of the experiment
        :ivar dict data: data object that contains all experiment info
        :return: Dictionary with loaded experiment info.
        """

        with open(os.path.join(experiment_path, 'experiment-settings.json'), 'r') as jsonfile:
            data = json.load(jsonfile)
            self.uuid4= data.uuid4 if data.uuid4 else self.uuid4
            self.name = data['name']
            self.task = data.get('task', None)

        for path in self.__list_all_setups_in_folder(experiment_path):
            setup = self.create_setup()
            setup.load(path, {})

        self.path = experiment_path



    def __clean_setups_path(self, experiment_path):
        # remove from the setups directory the unused setup files
        setups_paths = [setup.path for setup in self.setups]
        for path in self.__list_all_setups_in_folder(experiment_path):
            if path not in setups_paths:
                logger.debug("Sending directory [{0}] to trash".format(path))
                send2trash(path)

    def __generate_experiments_path(self, project_path):
        return os.path.join(project_path, 'experiments')

    def __generate_experiment_path(self, experiments_path):
        return os.path.join(experiments_path, self.name)

    def __list_all_setups_in_folder(self, experiment_path):
        search_4_dirs_path = os.path.join(experiment_path, 'setups')
        if not os.path.exists(search_4_dirs_path):
            return []
        return sorted([os.path.join(search_4_dirs_path, d) for d in os.listdir(search_4_dirs_path) if
                       os.path.isdir(os.path.join(search_4_dirs_path, d))])
