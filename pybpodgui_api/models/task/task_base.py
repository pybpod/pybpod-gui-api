# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os
from pybpodgui_plugin.utils.send2trash_wrapper import send2trash

logger = logging.getLogger(__name__)

class TaskBase(object):
	""" Represents a state machine """

	def __init__(self, project=None):
		self.name    = 'Untitled task {0}'.format( len(project.tasks) ) if project else None
		self.project = project
		self.path    = None
		self.project   += self
		
	##########################################################################
	####### PROPERTIES #######################################################
	##########################################################################

	@property
	def name(self): 
		return self._name
	   
	@name.setter
	def name(self, value): self._name = value

	@property
	def path(self): return self._path
	@path.setter
	def path(self, value): 
		self._path = value

	@property
	def code(self):
		if not self.path or not os.path.exists(self.path):
			raise FileNotFoundError("Task file not found!")
		with open(self.path, "r") as file: return file.read()
		return None
	@code.setter
	def code(self, value):
		if not self.path or not os.path.exists(self.path):
			tasks_path = os.path.join(self.project.path, 'tasks')
			if not os.path.exists(tasks_path): os.makedirs(tasks_path)

			task_folder = os.path.join(tasks_path, self.name)
			if not os.path.exists(task_folder): 
				os.makedirs(task_folder)

			initfile = os.path.join(task_folder, '__init__.py')
			if not os.path.exists(initfile): 
				with open(initfile, "w") as file: pass

			self.path = os.path.join(task_folder, self.name)+'.py'
		with open(self.path, "w") as file: file.write(value)

	@property
	def project(self):          return self._project
	@project.setter
	def project(self, project): self._project = project

	
	##########################################################################
	####### FUNCTIONS ########################################################
	##########################################################################

	def remove(self): pass
	
	def __unicode__(self):  return self.name
	def __str__(self):      return self.__unicode__()
