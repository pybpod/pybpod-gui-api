# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging, json
from pybpodgui_api.models.subject.subject_base import SubjectBase

logger = logging.getLogger(__name__)


class SubjectIO(SubjectBase):
	"""
	
	"""

	##########################################################################
	####### FUNCTIONS ########################################################
	##########################################################################

	
	def save(self, project_path):
		if not self.name:
			logger.warning("Skipping subject without name")
		else:
			subjects_path = os.path.join(project_path, 'subjects')
			if not os.path.exists(subjects_path): os.makedirs(subjects_path)

			subject_path = os.path.join(subjects_path, self.name)
			if not os.path.exists(subject_path):  os.makedirs(subject_path)

			data2save = {
				'name': self.name
			}
			settings_path = os.path.join(subject_path, 'subject-settings.json')
			with open(settings_path, 'w') as output_file:
				json.dump(data2save, output_file, sort_keys=False, indent=4, separators=(',', ':'))
			self.path = subject_path

			return data2save

	def load(self, subject_path, data):
		settings_path = os.path.join(subject_path, 'subject-settings.json')
		with open(settings_path, 'r') as output_file:
			data = json.load(output_file)
			
			self.name 		 = data['name']