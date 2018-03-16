# !/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import uuid
import subprocess 

from pyforms import conf
from pathlib import Path
from pybpodgui_plugin.com.async.async_bpod import AsyncBpod

from pybpodgui_api.models.setup import Setup
from pybpodgui_api.models.board.board_io import BoardIO
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

        # in case a session is running update the status of this sessions
        if not hasattr(self, '_running_session'): return

        session = self._running_session
        if value==self.STATUS_READY:
            session.status = session.STATUS_READY
        elif value==self.STATUS_RUNNING_TASK:
            session.status = session.STATUS_SESSION_RUNNING

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
        pass

    def log_session_history(self, msg):
        """
        Log session history on file and on memory.
        
        :ivar BaseMessage msg: Message to log.        
        """
        self._running_session.log_msg(msg)

    
    def run_task(self, session, board_task, workspace_path, detached=False):
        """
        Run a task.
        
        :ivar Session session: Session to record the data.  
        :ivar BoardTask board_task: Configuration to run session.  
        :ivar str workspace_path: Not used. To be removed in the future.  
        """
        
        self._running_task     = board_task.task
        self._running_session  = session
        
        if detached:
            Path(session.path).mkdir(parents=True, exist_ok=True) 
     
        else:
            session.open()

        board = board_task.board

        bpod_settings = """
from pyforms import conf

class RunnerSettings:
    SETTINGS_PRIORITY = 0
    WORKSPACE_PATH  =  {workspace_path}
    PROTOCOL_NAME   = '{session_name}.csv'
    SERIAL_PORT     = '{serialport}'
    NET_PORT        = {netport}

    {publish_func}

    {bnp_ports}
    {wired_ports}
    {behavior_ports}

conf += RunnerSettings
        """.format(
            workspace_path  = "'{0}'".format(session.path) if detached else None,
            serialport      = board.serial_port,
            bnp_ports       = ('BPOD_BNC_PORTS_ENABLED = {0}'.format(board.enabled_bncports)            if board.enabled_bncports else '') ,
            wired_ports     = ('BPOD_WIRED_PORTS_ENABLED = {0}'.format(board.enabled_wiredports)        if board.enabled_wiredports else '') ,
            behavior_ports  = ('BPOD_BEHAVIOR_PORTS_ENABLED = {0}'.format(board.enabled_behaviorports)  if board.enabled_behaviorports else ''),
            session_name    = session.name,
            publish_func    = 'PYBPOD_API_PUBLISH_DATA_FUNC = print' if not detached else '',
            netport         = board_task.setup.net_port
        )

        self.status = self.STATUS_RUNNING_TASK

        ## Execute the files before the task starts ################### 
        otherfiles = sorted(board_task.task.otherfiles, key=lambda x: x.name) 
        for ofile in otherfiles: 
            if ofile.execute: 
                if ofile.detached: 
                    subprocess.Popen(['python', ofile.filepath]) 
                else: 
                    global_dict = globals() 
                    global_dict['PYBPOD_PROJECT']      = session.project 
                    global_dict['PYBPOD_EXPERIMENT']   = session.setup.experiment 
                    global_dict['PYBPOD_BOARD']        = session.setup.board 
                    global_dict['PYBPOD_NETPORT']      = session.setup.net_port 
                    global_dict['PYBPOD_SETUP']        = session.setup 
                    global_dict['PYBPOD_SESSION']      = session 
                    global_dict['PYBPOD_SESSION_PATH'] = session.path 
                    global_dict['PYBPOD_SUBJECTS']     = session.setup.subjects 
                    exec(open(ofile.filepath, 'rb').read(), global_dict) 
        ############################################################### 

        AsyncBpod.run_protocol(self,
            bpod_settings,                              # settings
            board_task.task.filepath,                   # task file path
            'username',                                 # user running the task
            session.setup.experiment.project.name,      # project name
            session.setup.experiment.name,              # experiment name
            board_task.board.name,                      # board name
            session.setup.name,                         # setup name
            session.name,                               # session name
            session.path,                               # session path
            [s.name for s in session.setup.subjects],   # list of subjects
            [(v.name, v.value) for v in board_task.variables], # list of variables
            handler_evt=self.run_task_handler_evt,      # events handler: callend whenever there is something in the output queue
            extra_args=(detached, ),                    # call arguments
            group=uuid.uuid4()                          # unique identifier of this call
        )



    def run_task_handler_evt(self, evt, result):
        # flag to inform if the task is running detacted from the GUI or not.
        # in case it is detached no information is logged to the GUI.
        detached = evt.extra_args[0]

        try:
            if isinstance(result, Exception):
                self.log_msg_error(str(result))
                raise Exception("Unable to run protocol. Please check console for more info.")
            elif result is not None:
                if not detached:
                    self.log_msg(result)
                    self.log_session_history(result)

            if evt.last_call:
                if not detached: 
                    self._running_session.close()
                self.status           = self.STATUS_READY
                self._running_task    = None
                self._running_session = None
        except Exception as err:
            if not detached:
                self.log_session_history( StderrMessage(err) )
                self._running_session.close()


            self._running_task = None
            self._running_session = None
            self.status = self.STATUS_READY
            raise err
