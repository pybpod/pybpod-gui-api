# !/usr/bin/python3
# -*- coding: utf-8 -*-

""" pycontrol.api.models.project

"""
import logging
from pybpodgui_api.models.experiment import Experiment
from pybpodgui_api.models.board 		import Board
from pybpodgui_api.models.task 		import Task
from pybpodgui_api.models.subject 	import Subject


logger = logging.getLogger(__name__)


class ProjectBase(object):
	"""
	A project is a collection of experiments and an hardware configuration
	"""

	def __init__(self):
		"""
		:project_path: full path to project including project name
		"""
		self.name 			= ''
		self.path 			= None
		self._experiments 	= []
		self._tasks 		= []
		self._boards 		= []
		self._subjects 		= []

	##########################################################################
	####### PROPERTIES #######################################################
	##########################################################################

	@property
	def subjects(self):
		return self._subjects

	@property
	def experiments(self):
		return self._experiments

	@property
	def boards(self):
		return self._boards

	@property
	def tasks(self):
		return self._tasks

	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, value):
		self._path = value

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	##########################################################################
	####### FUNCTIONS ########################################################
	##########################################################################

	def __add__(self, obj):
		if isinstance(obj, Experiment): self._experiments.append(obj)
		if isinstance(obj, Board):      self._boards.append(obj)
		if isinstance(obj, Task):       self._tasks.append(obj)
		if isinstance(obj, Subject):    self._subjects.append(obj)
		return self

	def __sub__(self, obj):
		if isinstance(obj, Experiment): self._experiments.remove(obj)
		if isinstance(obj, Board):      self._boards.remove(obj)
		if isinstance(obj, Task):       self._tasks.remove(obj)
		if isinstance(obj, Subject):    self._subjects.remove(obj)
		return self

	def find_board(self, name):
		for board in self.boards:
			if board.name == name: return board
		return None

	def find_task(self, name):
		for task in self.tasks:
			if task.name == name: return task
		return None

	def find_subject(self, name):
		for subject in self.subjects:
			if subject.name == name: return subject
		return None

	def create_experiment(self):
		return Experiment(self)

	def create_board(self):
		return Board(self)

	def create_task(self):
		return Task(self)

	def create_subject(self):
		return Subject(self)
