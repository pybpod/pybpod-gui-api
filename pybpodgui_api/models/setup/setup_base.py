# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os
from pybpodgui_api.models.setup.board_task import BoardTask
from pybpodgui_api.models.session import Session
from pybpodgui_api.models.subject import Subject

logger = logging.getLogger(__name__)


class SetupBase(object):

	
	def __init__(self, experiment):
		self.experiment = experiment
		self.board_task = self.create_board_task()

		setup_path = None
		if experiment.path is not None:
			setups_path = os.path.join(experiment.path, 'setups')
			if not os.path.exists(setups_path): os.makedirs(setups_path)

			setup_path = os.path.join(setups_path, self.name)
			if not os.path.exists(setup_path): os.makedirs(setup_path)

		self.name = "Untitled box {0}".format(len(self.experiment.setups))
		self._sessions = []
		self._subjects = []
		self.path 	= setup_path
		self.board 	= None
		self.task 	= self.experiment.task

		self.experiment += self



	##########################################################################
	####### PROPERTIES #######################################################
	##########################################################################

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	@property
	def subjects(self):
		return self._subjects

	@property
	def board(self):
		return self.board_task.board

	@board.setter
	def board(self, value):
		if isinstance(value, str): value = self.project.find_board(value)
		if self.board_task: self.board_task.board = value

	@property
	def task(self):
		return self.board_task.task

	@task.setter
	def task(self, value):
		if isinstance(value, str): value = self.project.find_task(value)
		if self.board_task: self.board_task.task = value

	@property
	def experiment(self):
		return self._experiment

	@experiment.setter
	def experiment(self, value):
		self._experiment = value

	@property
	def project(self):
		return self.experiment.project

	@property
	def sessions(self):
		return self._sessions

	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, value):
		self._path = value

	@property
	def last_session(self):
		try:
			order_sessions = sorted(self.sessions, key=lambda session: session.started)  # sort by end_date
			return order_sessions[-1]
		except IndexError as err:
			return None

	##########################################################################
	####### FUNCTIONS ########################################################
	##########################################################################

	def remove(self):
		pass

	def create_board_task(self):
		return BoardTask(self)

	def create_session(self):
		return Session(self)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.__unicode__()

	def __add__(self, obj):
		if isinstance(obj, Session) and obj not in self._sessions: self._sessions.append(obj)
		if isinstance(obj, Subject) and obj not in self._subjects: self._subjects.append(obj)
		return self

	def __sub__(self, obj):
		if isinstance(obj, Session): self._sessions.remove(obj)
		if isinstance(obj, Subject): self._subjects.remove(obj)
		return self
