# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging, json
from pybpodgui_api.models.board.board_base import BoardBase

logger = logging.getLogger(__name__)


class BoardIO(BoardBase):
	"""
	
	"""

	def __init__(self, project):
		super(BoardIO, self).__init__(project)
	
	##########################################################################
	####### FUNCTIONS ########################################################
	##########################################################################

	def collect_data(self, data):
		data.update({'name': self.name})
		data.update({'serial_port': self.serial_port})

		return data

	def save(self, parent_path):
		if not self.name:
			logger.warning("Skipping board without name")
		else:
			boards_path = self.__generate_boards_path(parent_path)
			if not os.path.exists(boards_path):
				os.makedirs(boards_path)

			board_path = self.__generate_board_path(boards_path)
			if not os.path.exists(board_path):
				os.makedirs(board_path)

			data2save = {
				'name': 					self.name,
				'serial_port': 	 			self.serial_port,
				'enabled-bncports': 		self.enabled_bncports,
				'enabled-wiredports': 		self.enabled_wiredports,
				'enabled-behaviorports':	self.enabled_behaviorports,
			}

			self.__save_on_file(data2save, board_path, 'board-settings.json')

			self.path = board_path

			return data2save

	def load(self, board_path, data):
		settings_path = os.path.join(board_path, 'board-settings.json')
		with open(settings_path, 'r') as output_file:
			data = json.load(output_file)
			
			self.name 		 = data['name']
			self.serial_port = data['serial_port']
			self._path 		 = board_path

			self.enabled_bncports 		= data.get('enabled-bncports', 		None)
			self.enabled_wiredports 	= data.get('enabled-wiredports', 	None)
			self.enabled_behaviorports = data.get('enabled-behaviorports', None)

			

	def __generate_boards_path(self, project_path):
		return os.path.join(project_path, 'boards')

	def __generate_board_path(self, boards_path):
		return os.path.join(boards_path, self.name)

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
