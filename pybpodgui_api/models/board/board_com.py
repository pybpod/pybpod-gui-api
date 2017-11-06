# !/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import uuid

from pysettings import conf

from pybpodgui_plugin.com.async.async_bpod import AsyncBpod

from pybpodgui_api.models.board.board_io import BoardIO
from pybpodgui_api.models.board.board_operations import BoardOperations
from pybpodgui_api.com.messaging.msg_factory import parse_board_msg
from pybpodgui_api.models.setup.board_task import BoardTask  # used for type checking

from pybranch.com.messaging.stderr import StderrMessage

logger = logging.getLogger(__name__)


class BoardCom(AsyncBpod, BoardIO):
    #### SETUP STATUS ####
    STATUS_READY = 0
    STATUS_RUNNING_TASK = 1  # The board is busy running a task

    def __init__(self, project):
        BoardIO.__init__(self, project)
        AsyncBpod.__init__(self)
        self.status = BoardCom.STATUS_READY

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def status(self):
        """
        Get and set the board status

        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def log_msg(self, msg):
        """
        Add a message to the board.

        :ivar BaseMessage msg: Message to log.
        """
        parsed_messages = parse_board_msg(msg)
        for m in parsed_messages:
            self.log_messages.append(m)

    def log_session_history(self, msg):
        """
        Log session history on file and on memory.
        
        :ivar BaseMessage msg: Message to log.        
        """
        self._running_session.log_msg(msg)

    
    def run_task(self, session, board_task, workspace_path):
        """
        Run a task.
        
        :ivar Session session: Session to record the data.  
        :ivar BoardTask board_task: Configuration to run session.  
        :ivar str workspace_path: Not used. To be removed in the future.  
        """
        
        self._session_log_file  = open(session.path, 'w+', newline='\n', buffering=1) 
        self._running_task      = board_task.task
        self._running_session   = session
        session.open()

        board = board_task.board

        bpod_settings = """
from pysettings import conf

class RunnerSettings:
    SETTINGS_PRIORITY = 0
    WORKSPACE_PATH  = None
    PROTOCOL_NAME   = '{protocolname}'
    SERIAL_PORT     = '{serialport}'

    PYBPOD_API_PUBLISH_DATA_FUNC = print

    {bnp_ports}
    {wired_ports}
    {behavior_ports}

conf += RunnerSettings
        """.format(
            serialport      = board.serial_port,
            bnp_ports       = ('BPOD_BNC_PORTS_ENABLED = {0}'.format(board.enabled_bncports)            if board.enabled_bncports else '') ,
            wired_ports     = ('BPOD_WIRED_PORTS_ENABLED = {0}'.format(board.enabled_wiredports)        if board.enabled_wiredports else '') ,
            behavior_ports  = ('BPOD_BEHAVIOR_PORTS_ENABLED = {0}'.format(board.enabled_behaviorports)  if board.enabled_behaviorports else ''),
            protocolname    = board_task.task.name
        )

        AsyncBpod.run_protocol(self,
            bpod_settings,
            board_task.task.path,
            'username',
            session.setup.experiment.project.name,
            session.setup.experiment.name,
            board_task.board.name,
            session.setup.name,
            [s.name for s in session.setup.subjects],
            [(v.name, v.value) for v in board_task.variables],
            handler_evt=self.run_task_handler_evt,
            extra_args=(BoardOperations.RUN_PROTOCOL,),
            group=uuid.uuid4()
        )



    def run_task_handler_evt(self, e, result):
        called_operation = e.extra_args[0]

        try:
            if called_operation == BoardOperations.RUN_PROTOCOL:
                if isinstance(result, Exception):
                    self.log_msg_error(str(result))
                    raise Exception("Unable to run protocol. Please check console for more info.")
                elif result is not None:
                    self.log_msg(result)
                    self.log_session_history(result)

            if e.last_call:
                self._running_session.close() 
                self._running_task = None
                self._running_session = None
        except Exception as err:
            self.log_session_history( StderrMessage(err) )
            self._running_session.close() 

            #if self._running_session:
            #   self._running_session.setup.stop_task()

            self._running_task = None
            self._running_session = None
            raise err
