# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os
from pybpodgui_api.models.task.task_base import TaskBase

logger = logging.getLogger(__name__)


class TaskIO(TaskBase):
	"""
	Task I/O operations
	"""

	def __init__(self, project=None):
		super(TaskIO, self).__init__(project)

	##########################################################################
	####### FUNCTIONS ########################################################
	##########################################################################

	def save(self, project_path, data):
		"""
		
		:param str project_path: 
		:param dict data: 
		"""
		# save only if the task file exists
		tasks_path = os.path.join(project_path, 'tasks')
		if not os.path.exists(tasks_path): os.makedirs(tasks_path)

		task_folder = os.path.join(tasks_path, self.name)
		if not os.path.exists(task_folder): os.makedirs(task_folder)

		new_task_path = os.path.join(task_folder, self.name) + '.py'

		if self.path != new_task_path:
			# if the task file is not in the project file, it makes a copy to the project folder
			code_txt = self.code if self.path else ''
			self.path = new_task_path
			self.code = code_txt


	def load(self, task_path, data):
		"""
		
		:param str task_path: 
		:param dict data: 
		"""

		self.name = os.path.splitext(os.path.basename(task_path))[0]
		self.path = task_path
