# !/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import uuid
import subprocess
#import fcntl
import os, io
import sys
import pickle
import base64
import marshal
import pandas as pd

from AnyQt.QtCore import QTimer
from pyforms import conf
from pathlib import Path
from pybpodgui_plugin.com.async.async_bpod import AsyncBpod

from pybpodgui_api.models.setup import Setup
from pybpodgui_api.models.board.board_io import BoardIO
from pybpodgui_api.models.setup.board_task import BoardTask  # used for type checking

from pybpodgui_api.com.messaging.parser         import BpodMessageParser

from pybpodapi.com.messaging.stdout import StdoutMessage
from pybpodapi.com.messaging.stderr import StderrMessage

from sca.formats import csv

from .non_blockingcsvreader import NonBlockingCSVReader

logger = logging.getLogger(__name__)


class BoardCom(AsyncBpod, BoardIO):
    #### SETUP STATUS ####
    STATUS_READY = 0
    STATUS_RUNNING_TASK = 1  # The board is busy running a task


    INFO_CREATOR_NAME       = 'CREATOR-NAME'
    INFO_PROJECT_NAME       = 'PROJECT-NAME'
    INFO_EXPERIMENT_NAME    = 'EXPERIMENT-NAME'
    INFO_BOARD_NAME         = 'BOARD-NAME'
    INFO_SETUP_NAME         = 'SETUP-NAME'
    INFO_SUBJECT_NAME       = 'SUBJECT-NAME'
    INFO_BPODGUI_VERSION    = 'BPOD-GUI-VERSION'

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

    def pause_trial(self):
        if hasattr(self, 'proc'):
            self.proc.stdin.write("pause-trial\r\n".encode())
            self.proc.stdin.flush()

    def resume_trial(self):
        if hasattr(self, 'proc'):
            self.proc.stdin.write("resume-trial\r\n".encode())
            self.proc.stdin.flush()

    def stop_trial(self):
        if hasattr(self, 'proc'):
            self.proc.stdin.write("stop-trial\r\n".encode())
            self.proc.stdin.flush()

    def stop_task(self):
        if hasattr(self, 'proc'):
            self.proc.stdin.write("close\r\n".encode())
            self.proc.stdin.flush()

    
            
    
    def run_task(self, session, board_task, workspace_path, detached=False):
        """
        Run a task.
        
        :ivar Session session: Session to record the data.  
        :ivar BoardTask board_task: Configuration to run session.  
        :ivar str workspace_path: Not used. To be removed in the future.  
        """
        
        self._running_task     = board_task.task
        self._running_session  = session
        
        board = board_task.board

        # create the session path
        Path(session.path).mkdir(parents=True, exist_ok=True) 
        
        # load bpod configuration template
        template      = os.path.join(os.path.dirname(__file__), 'run_settings_template.py')
        bpod_settings = open(template, 'r').read().format(
            workspace_path  = "'{0}'".format(os.path.abspath(session.path) ),
            serialport      = board.serial_port,
            bnp_ports       = ('BPOD_BNC_PORTS_ENABLED = {0}'.format(board.enabled_bncports)            if board.enabled_bncports else '') ,
            wired_ports     = ('BPOD_WIRED_PORTS_ENABLED = {0}'.format(board.enabled_wiredports)        if board.enabled_wiredports else '') ,
            behavior_ports  = ('BPOD_BEHAVIOR_PORTS_ENABLED = {0}'.format(board.enabled_behaviorports)  if board.enabled_behaviorports else ''),
            session_name    = session.name,
            publish_func    = 'PYBPOD_API_PUBLISH_DATA_FUNC = print' if not detached else '',
            netport         = board_task.board.net_port,

            project         = session.project.name,
            experiment      = session.setup.experiment.name,
            board           = board_task.board.name,
            setup           = session.setup.name,
            session         = session.name,
            session_path    = session.path,
            subjects        = ','.join( list(map(lambda x: "'"+x+"'", session.subjects)) )
        )
        """
        var.session += SessionInfo(self.INFO_CREATOR_NAME,      user_name)  # TODO
        var.session += SessionInfo(self.INFO_PROJECT_NAME,      project_name)   
        var.session += SessionInfo(self.INFO_EXPERIMENT_NAME,   experiment_name)
        var.session += SessionInfo(self.INFO_SETUP_NAME, setup_name)
        var.session += SessionInfo(var.session.INFO_SESSION_ENDED, datetime_now.now())
        for subject in subjects: var.session += SessionInfo(self.INFO_SUBJECT_NAME, subject)
        var.session += SessionInfo(self.INFO_BPODGUI_VERSION, pybpodgui_plugin.__version__)
        """        

        #create the bpod configuration file in the session folder
        settings_path = os.path.join(self._running_session.path,'user_settings.py')
        with open(settings_path, 'w' ) as out: out.write(bpod_settings) 

        #create the bpod configuration file in the session folder
        init_path = os.path.join(self._running_session.path,'__init__.py')
        with open(init_path, 'w' ) as out: pass


        ## Execute the PRE commands ################################### 
        for cmd in board_task.task.commands:
            if cmd.when==0:
                cmd.execute(session=session)
        ############################################################### 

        task = board_task.task

        
        self.start_run_task_handler()

        enviroment = os.environ.copy()
        enviroment['PYTHONPATH'] = ":".join([os.path.abspath(self._running_session.path)]+sys.path)
        
        session.data = pd.DataFrame(columns=['TYPE','PC-TIME','BPOD-INITIAL-TIME','BPOD-FINAL-TIME','MSG','+INFO'])

        self.proc = subprocess.Popen(
            ['python', os.path.abspath(task.filepath)],
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            cwd=self._running_session.path,
            env=enviroment
        )

        """
        # make stdin a non-blocking file
        fd = self.proc.stdin.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        # make stdin a non-blocking file
        fd = self.proc.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        # make stdin a non-blocking file
        fd = self.proc.stderr.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        """
        
        
        self.csvreader = NonBlockingCSVReader( 
            csv.reader( io.TextIOWrapper(self.proc.stdout, encoding='utf-8') )
        )
        
    def run_task_handler(self, flag=True):
        if flag and self.proc.poll() is not None: self.end_run_task_handler()
        
        row = self.csvreader.readline()
        while row is not None:
            if row is None: break
            self._running_session.data.loc[len(self._running_session.data)] = row
            row = self.csvreader.readline()

            
            #self._running_session.data.loc[len(self._running_session.data)] = row
            #msg = BpodMessageParser.fromlist(row)
            #self._running_session += msg
            #self += msg
        

    def start_run_task_handler(self):
        self.status = self.STATUS_RUNNING_TASK

    def end_run_task_handler(self):
        del self.proc


        ## Execute the POST commands ################################## 
        #for cmd in self._running_task.commands:
        #    if cmd.when==1:
        #        cmd.execute(session=self._running_session)
        ############################################################### 

        self.status = self.STATUS_READY

