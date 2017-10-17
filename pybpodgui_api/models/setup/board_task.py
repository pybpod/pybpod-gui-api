# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from pybpodgui_api.exceptions.invalid_task import InvalidTaskError
from pybpodgui_api.models.task_variable import TaskVariable

logger = logging.getLogger(__name__)


class BoardTask(object):
	"""
	Represents the association between one board and one task
	"""

	def __init__(self, setup):
		self.setup = setup

		self.variables = []
		self.states = {}
		self.events = {}
		self.board = None
		self.task = None
		self.highest_state_id = 0

	##########################################################################
	####### PROPERTIES #######################################################
	##########################################################################

	@property
	def board(self):
		return self._board

	@board.setter
	def board(self, value):
		self._board = value

	@property
	def task(self):
		return self._task

	@task.setter
	def task(self, value):
		self._task = value

	@property
	def variables(self):
		return self._variables  # type: list(TaskVariable)

	@variables.setter
	def variables(self, value):
		self._variables = value

	@property
	def states(self):
		return self._states

	@states.setter
	def states(self, value):
		self._states = value

		if len(value) > 0:
			self.highest_state_id = sorted(map(int, value.keys()))[-1]

	@property
	def events(self):
		return self._events

	@events.setter
	def events(self, value):
		self._events = value

	##########################################################################
	####### FUNCTIONS ########################################################
	##########################################################################

	def create_variable(self, name=None, value=None, persistent=False):
		return TaskVariable(name, value, persistent)

	def collect_data(self, data):
		data.update({'states': self.states})
		data.update({'events': self.events})
		data.update({'variables': []})
		for var in self.variables:
			data['variables'].append(var.collect_data({}))

		return data

	def save(self):

		# collect variables data
		variables_data = [var.save() for var in self.variables]

		data2save = {}
		data2save.update({'states': self.states})
		data2save.update({'events': self.events})
		data2save.update({'variables': variables_data})

		return data2save

	def load(self, setup_path, data):
		variables_data = data.get('variables', [])

		self.events = data.get('events', {})
		self.states = data.get('states', {})

		variables = []
		for var_data in variables_data:
			value = None if var_data['value'] == 'None' else var_data['value']
			var = self.create_variable(var_data['name'], value, var_data['persistent'] == 'True')
			variables.append(var)

		self.variables = variables

	def load_task_details(self):
		if self.task:
			self.states = self.task.find_states_from_file()
			self.events = self.task.find_events_from_file(len(self.states) + 1)
			self.variables = [self.create_variable(var_name, var_value) for (var_name, var_value) in
			                  self.task.find_task_variables_from_file()]

	def set_variable(self, name, value):
		variables = self.variables
		var = self.find_variable_by_name(name, variables)
		if var: var.value = value
		self.variables = variables

	def find_variable_by_name(self, var_name, variables=None):
		for var in variables if variables else self.variables:
			if var.name == var_name: return var
		return None

	def is_state_change(self, event_id):
		"""
		Checks if event_id is a state change or a fired event
		:param event_id: event id
		:type event_id: integer
		"""
		try:
			return event_id <= self.highest_state_id
		except AttributeError as err:
			raise InvalidTaskError("Task lowest event id is not set", err)
		return False

	def __unicode__(self):
		return "Board : {board} | Task: {task}".format(board=str(self.board), task=str(self.task))

	def __str__(self):
		return self.__unicode__()
