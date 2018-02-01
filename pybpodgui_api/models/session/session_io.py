# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os, datetime, dateutil, shutil

from pybpodgui_api.models.session.session_base  import SessionBase
from pybpodgui_api.exceptions.invalid_session   import InvalidSessionError

from pybpodgui_api.com.messaging.msg_factory import BpodMessageParser


from pybpodapi.session import Session
from pybpodapi.com.messaging.session_info import SessionInfo
from pybpodgui_plugin.com.run_handlers.bpod_runner import BpodRunner

from sca.formats import csv 


class SessionIO(SessionBase):
    """

    """

    def __init__(self, setup):
        super(SessionIO, self).__init__(setup)


    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def save(self, repository):
        """

        :param parent_path:
        :return:
        """
        repository.add_file( self.filepath , self.name+'.csv')
        repository['name'] = self.name
        repository.save()

        self.name = repository.name
        self.filepath = os.path.join(self.path, self.name+'.csv')


    def load(self, repository):
        """

        :param session_path:
        :param data:
        :return:
        """
        self.name   = repository.name
        self.uuid4  = repository.uuid4 if repository.uuid4 else self.uuid4
        self.filepath = os.path.join(self.path, self.name+'.csv')

    def load_contents(self, session_path):
        """
        Parses session history file, line by line and populates the history message on memory.

        :param str session_path: path to session history file
        """

        parser = BpodMessageParser()
        with open(session_path) as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                msg = parser.fromlist(row)
                if msg:
                    self.messages_history.append(msg)

                    if isinstance(msg, SessionInfo):
                        if   msg.infoname==Session.INFO_PROTOCOL_NAME:
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



                    