# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os, csv, datetime, dateutil

from pybpodgui_api.models.session.session_base 	import SessionBase
from pybpodgui_api.exceptions.invalid_session 	import InvalidSessionError

from pybpodgui_api.com.messaging.msg_factory import BpodMessageParser


from pybpodapi.session import Session
from pybpodapi.com.messaging.session_info import SessionInfo
from pybpodgui_plugin.com.run_handlers.bpod_runner import BpodRunner


class SessionIO(SessionBase):
	"""

	"""

	def __init__(self, setup):
		super(SessionIO, self).__init__(setup)


	##########################################################################
	####### FUNCTIONS ########################################################
	##########################################################################

	def save(self, parent_path):
		"""

		:param parent_path:
		:return:
		"""
		filename = os.path.basename(self.path).replace('.txt', '')
		filepath = os.path.dirname(self.path)

		if filename != self.name or filepath != parent_path:
			new_path = os.path.join(parent_path, self.name + '.txt')
			os.rename(self.path, new_path)
			self.path = new_path

	def load(self, session_path, data):
		"""

		:param session_path:
		:param data:
		:return:
		"""
		self.name = os.path.basename(session_path).replace('.txt', '')
		self.path = session_path

	def load_contents(self, session_path):
		"""
		Parses session history file, line by line and populates the history message on memory.

		:param str session_path: path to session history file
		"""

		parser = BpodMessageParser()
		with open(session_path, 'r', newline='\n') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for row in csvreader:
				msg = parser.fromlist(row)
				if msg:
					self.messages_history.append(msg)


					if isinstance(msg, SessionInfo):
						if 	 msg.infoname==Session.INFO_PROTOCOL_NAME:
							self.task_name = msg.infovalue

						elif msg.infoname==Session.INFO_SESSION_STARTED:
							self.started = dateutil.parser.parse(msg.infovalue)

						elif msg.infoname==Session.INFO_SESSION_ENDED:
							self.ended = dateutil.parser.parse(msg.infovalue)

						elif msg.infoname==Session.INFO_SERIAL_PORT:
							self.board_serial_port = msg.infovalue

						elif msg.infoname==BpodRunner.INFO_BOARD_NAME:
							self.board_name = msg.infovalue

						elif msg.infoname==BpodRunner.INFO_SETUP_NAME:
							self.setup_name = msg.infovalue

						elif msg.infoname==BpodRunner.INFO_SUBJECT_NAME:
							subjects = self.subjects
							subjects.append( msg.infovalue )
							self.subjects = subjects



					
