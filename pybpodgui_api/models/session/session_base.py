# !/usr/bin/python3
# -*- coding: utf-8 -*-


import os, csv, datetime, logging
from pybpodgui_plugin.com.messaging.msg_factory import parse_board_msg, BpodMessageParser

logger = logging.getLogger(__name__)


class SessionBase(object):
	"""
	Represents a board running session
	"""

	def __init__(self, setup):
		setup += self
		self.setup 				= setup
		self.name 				= datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
		self.path 				= os.path.join(self.setup.path, "{0}.txt".format(self.name))
		self.setup_name 		= setup.name
		self.board_name 		= setup.board.name if setup.board else None
		self.task_name 			= setup.task.name if setup.task else None
		self.board_serial_port 	= setup.board.serial_port if setup.board else None
		self.started 			= datetime.datetime.now()
		self.ended 				= None
		self.messages_history 	= []
		self.subjects 			= []


	def open(self):
		self.csvfile 	= open(self.path, 'w+', newline='\n', buffering=1)
		self.csvwriter 	= csv.writer(self.csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	def close(self):
		self.csvfile.close()

	def log_msg(self, msg): 
		""" 
		Parses board output and creates new session history entry 
	 
		:param msg: message to be parsed 
		:param file_obj: file object reference to write output to session history file 
		""" 
		parsed_messages = parse_board_msg(msg) 

		for m in parsed_messages: 
			self.csvwriter.writerow(m.tolist()) 
			self.messages_history.append(m) 
		
		

	##########################################################################
	####### PROPERTIES #######################################################
	##########################################################################


	def remove(self):
		pass

	

	@property
	def setup(self):
		return self._setup

	@setup.setter
	def setup(self, value):
		self._setup = value

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, value):
		self._path = value

	@property
	def setup_name(self):
		return self._setup_name

	@setup_name.setter
	def setup_name(self, value):
		self._setup_name = value

	@property
	def board_name(self):
		return self._board_name

	@board_name.setter
	def board_name(self, value):
		self._board_name = value

	@property
	def task_name(self):
		return self._task_name

	@task_name.setter
	def task_name(self, value):
		self._task_name = value

	@property
	def board_serial_port(self):
		return self._board_serial_port

	@board_serial_port.setter
	def board_serial_port(self, value):
		self._board_serial_port = value

	@property
	def started(self):
		return self._started

	@started.setter
	def started(self, value):
		self._started = value

	@property
	def ended(self):
		return self._ended

	@ended.setter
	def ended(self, value):
		self._ended = value

	@property
	def messages_history(self):
		return self._messages_history

	@messages_history.setter
	def messages_history(self, value):
		self._messages_history = value

	@property
	def project(self):
		return self.setup.project

	@property
	def task(self):
		return self.setup.task
