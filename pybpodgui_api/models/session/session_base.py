# !/usr/bin/python3
# -*- coding: utf-8 -*-


import os, csv, datetime, logging, dateutil
from pybpodapi.session import Session
from pybpodapi.com.messaging.session_info import SessionInfo
from pybpodgui_api.com.messaging.msg_factory import parse_board_msg, BpodMessageParser

logger = logging.getLogger(__name__)


class SessionBase(object):
    """
    Represents a board running session
    """

    def __init__(self, setup):
        setup += self
        self.setup              = setup
        self.name               = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        self.path               = os.path.join(self.setup.path, "{0}.txt".format(self.name))
        self.setup_name         = setup.name
        self.board_name         = setup.board.name if setup.board else None
        self.task_name          = setup.task.name if setup.task else None
        self.board_serial_port  = setup.board.serial_port if setup.board else None
        self.started            = datetime.datetime.now()
        self.ended              = None
        self.messages_history   = []
        self.subjects           = []


    def open(self):
        """
        Open the csv file to write the session data
        """
        self.csvfile    = open(self.path, 'w+', newline='\n', buffering=1)
        self.csvwriter  = csv.writer(self.csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def close(self):
        """
        llose the session csv file
        """
        self.csvfile.close()

    def log_msg(self, msg): 
        """ 
        Parses board output and creates new session history entry 

        :ivar BaseMessage msg: message to be parsed 
        """ 
        parsed_messages = parse_board_msg(msg) 

        for m in parsed_messages: 
            if isinstance(m, SessionInfo) and m.infoname==Session.INFO_SESSION_ENDED:
                self.ended = m.infovalue

            self.csvwriter.writerow(m.tolist()) 
            self.messages_history.append(m) 
        
        

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################


    def remove(self):
        """
        Remove the session from the project

        """
        pass
    

    @property
    def setup(self):
        """
        Get and set the setup

        :rtype: Setup
        """
        return self._setup

    @setup.setter
    def setup(self, value):
        self._setup = value

    @property
    def name(self):
        """
        Get and set session name

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def path(self):
        """
        Get and set path name

        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def setup_name(self):
        """
        Get and set setup name

        :rtype: str
        """
        return self._setup_name

    @setup_name.setter
    def setup_name(self, value):
        self._setup_name = value

    @property
    def board_name(self):
        """
        Get and set board name

        :rtype: str
        """
        return self._board_name

    @board_name.setter
    def board_name(self, value):
        self._board_name = value

    @property
    def task_name(self):
        """
        Get and set the task name

        :rtype: str
        """
        return self._task_name

    @task_name.setter
    def task_name(self, value):
        self._task_name = value

    @property
    def board_serial_port(self):
        """
        Get and set board serial port

        :rtype: str
        """
        return self._board_serial_port

    @board_serial_port.setter
    def board_serial_port(self, value):
        self._board_serial_port = value

    @property
    def started(self):
        """
        Get and set the start datetime of the session

        :rtype: datetime.datetime
        """
        return self._started

    @started.setter
    def started(self, value):
        self._started = value

    @property
    def ended(self):
        """
        Get and set the end datetime of the session

        :rtype: datetime.datetime
        """
        return self._ended

    @ended.setter
    def ended(self, value):
        self._ended = value

    @property
    def messages_history(self):
        """
        Get and set the history of messages

        :rtype: list(BaseMessage)
        """
        return self._messages_history

    @messages_history.setter
    def messages_history(self, value):
        self._messages_history = value

    @property
    def project(self):
        """
        Get the session Project

        :rtype: Project
        """
        return self.setup.project

    @property
    def task(self):
        """
        Get the session Task

        :rtype: Task
        """
        return self.setup.task