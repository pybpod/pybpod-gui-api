# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pybpodgui_api.exceptions.run_setup import RunSetupError
from pybpodgui_api.models.setup.setup_io import SetupBaseIO

from time import sleep

logger = logging.getLogger(__name__)


class SetupCom(SetupBaseIO):
	"""
	Define board actions that are triggered by setup.

	**Properties**

		status
			:class:`int`

			Holds setup status depending on board communication state.

	**Methods**

	"""

	#### SETUP STATUS CONSTANTS ####
	STATUS_READY 		= 0
	STATUS_BOARD_LOCKED = 1 # The setup is free but the board is busy
	STATUS_RUNNING_TASK = 2 # The setup is busy running the task, but it cannot be stopped yet
	


	def __init__(self, experiment):
		super(SetupCom, self).__init__(experiment)
		self.status = self.STATUS_READY

	##########################################################################
	####### PROPERTIES #######################################################
	##########################################################################

	@property
	def status(self):
		return self._status

	@status.setter
	def status(self, value):
		self._status = value

		print('sssss', value)

	##########################################################################
	####### FUNCTIONS ########################################################
	##########################################################################


	def run_task(self):
		"""
		Run task on board.

		In order to run task, the project must be saved before.
		This method will restore task variables from session, create a new session
		and start the 'run task' operation by calling board function run_task.

		"""
		if not self.project.is_saved():
			logger.warning("Run protocol cannot be executed because project is not saved.")
			raise RunSetupError("Project must be saved before run protocol")

		if not self.board or not self.task:
			logger.warning("Setup has no protocol assigned.")
			raise RunSetupError("Please assign a board and protocol first")

		try:
			print('run--------')
			# update the status of the setup
			self.status = self.STATUS_RUNNING_TASK

			session = self.create_session()

			self._run_flag = self.board.run_task(
				session, 
				self.board_task, 
				self.path, 
				detached=self.detached
			)

		except Exception as err:
			logger.error(str(err), exc_info=True)
			raise Exception("Unknown error found while running task. See log for more details.")

	
	def stop_task(self):
		pass