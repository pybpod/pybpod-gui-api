# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os, json, hashlib
from pybpodgui_plugin.utils.send2trash_wrapper import send2trash
from pybpodgui_api.models.experiment.experiment_base import ExperimentBase

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
		Save experiment data on filesystem
		:param parent_path: path to project
		:param data: data object that contains all project info
		"""
		experiments_path = self.__generate_experiments_path(parent_path)
		if not os.path.exists(experiments_path):
			os.makedirs(experiments_path)

		experiment_path = self.__generate_experiment_path(experiments_path)
		if not os.path.exists(experiment_path):
			os.makedirs(experiment_path)

		# save setups
		for setup in self.setups:
			setup.save(parent_path=experiment_path)

		data2save = {
			'name': self.name,
			'task': self.task.name if self.task else None
		}

		self.path = experiment_path

		self.__clean_setups_path(experiment_path)  # call only after update setups

		self.__save_on_file(data2save, dest_path=experiment_path, filename='experiment-settings.json')

		return data2save

	def load(self, experiment_path, data):
		"""
		Load experiment data from filesystem
		:param experiment_path:
		:param data: data object that contains all project info
		:return: data object augmented with experiment info
		"""
		settings_path = os.path.join(experiment_path, 'experiment-settings.json')
		with open(settings_path, 'r') as output_file:
			data = json.load(output_file)

			self.name = data['name']
			self.task = data.get('task', None)

			for path in self.__list_all_setups_in_folder(experiment_path):
				setup = self.create_setup()
				setup.load(path, {})

			self.path = experiment_path

		return data

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
