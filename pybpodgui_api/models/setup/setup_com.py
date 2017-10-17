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
	STATUS_READY = 0
	STATUS_BOARD_LOCKED = 1  # The setup is free but the board is busy
	STATUS_INSTALLING_TASK = 2  # The setup is busy installing the board
	STATUS_SYNCING_VARS = 3  # The setup is syncing variables
	STATUS_RUNNING_TASK = 4  # The setup is busy running the task, but it cannot be stopped yet
	STATUS_RUNNING_TASK_HANDLER = 5  # The setup is busy running the task, but it is possible to stopped it
	STATUS_RUNNING_TASK_ABOUT_2_STOP = 6  # The setup is busy running the task, but it is about to stop it

	def __init__(self, experiment):
		super(SetupCom, self).__init__(experiment)
		self.status = SetupCom.STATUS_READY

	##########################################################################
	####### PROPERTIES #######################################################
	##########################################################################

	@property
	def status(self):
		try:
			if self.board is not None and self.board.status == self.board.STATUS_INSTALLING_FRAMEWORK:
				return SetupCom.STATUS_BOARD_LOCKED
			else:
				return self._status
		except Exception as e:
			logger.error(str(e), exc_info=True)

	@status.setter
	def status(self, value):
		self._status = value

		if value == SetupCom.STATUS_READY:
			if hasattr(self, '_run_flag'): del self._run_flag

	##########################################################################
	####### FUNCTIONS ########################################################
	##########################################################################


	def run_task(self):
		"""
		Run task on board.

		In order to run task, the project must be saved before.
		This method will restore task variables from session, create a new session
		and start the 'run task' operation by calling board function run_task.

		.. seealso:
			:py:meth:`pycontrolgui.models.board.board_com.BoardCom.run_task`.

		"""
		if not self.project.is_saved():
			logger.warning("Run protocol cannot be executed because project is not saved.")
			raise RunSetupError("Project must be saved before run protocol")

		if not self.board or not self.task:
			logger.warning("Setup has no protocol assigned.")
			raise RunSetupError("Please assign a board and protocol first")

		try:
			session = self.create_session()

			self._run_flag = self.board.run_task(session, self.board_task, self.path)
		except Exception as err:
			logger.error(str(err), exc_info=True)
			raise Exception("Unknown error found while running task. See log for more details.")

	def stop_task(self):
		"""
		Stop task on board.

		Update setup status to STATUS_RUNNING_TASK_ABOUT_2_STOP and try to stop board.

		"""
		if hasattr(self, '_run_flag') and self._run_flag:
			self.status = SetupCom.STATUS_RUNNING_TASK_ABOUT_2_STOP
			self.board.write(b'E') # Serial command to stop run.
			sleep(0.1)
			self._run_flag.set()

