# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os, datetime, dateutil, shutil

from pybpodgui_api.models.session.session_base  import SessionBase
from pybpodgui_api.exceptions.invalid_session   import InvalidSessionError
from pybpodgui_api.com.messaging.parser         import BpodMessageParser


from pybpodapi.session import Session
from pybpodapi.com.messaging.session_info import SessionInfo

from sca.formats import csv
import pandas as pd

class SessionIO(SessionBase):
    """

    """



    def __init__(self, setup):
        super(SessionIO, self).__init__(setup)

        # repository that will manage the project files
        self.repository = None


    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def save(self, parent_repository):
        """

        :param parent_path:
        :return:
        """    
        oldname = os.path.basename(os.path.dirname(self.filepath)) if self.filepath else self.name
  
        # if the project was loaded then it will reuse the repository otherwise create a new repository ################################
        repository = self.repository = self.repository if self.repository else parent_repository.sub_repository('sessions', oldname, uuid4=self.uuid4, fileformat='csv')
        ################################################################################################################################

        repository.fileformat = 'csv'
        repository.uuid4   = self.uuid4
        repository.name    = self.name
        repository.commit()

        """
        #repository.save()
        oldfolder = os.path.dirname(self.filepath)
        if os.path.exists(self.filepath):
            os.rename(self.filepath, os.path.join(self.path, self.name+'.csv') )
            self.filepath = os.path.join(self.path, self.name+'.csv')
        os.rename(oldfolder, self.path)
        """
        return repository
        

    def load(self, repository):
        """

        :param session_path:
        :param data:
        :return:
        """
        self.repository = repository
        self.name       = repository.name

        # only set the filepath if it exists
        filepath      = os.path.join(self.path, self.name+'.csv')
        self.filepath = filepath if os.path.exists(filepath) else None

        try:
            self.load_info()
        except FileNotFoundError:
            pass



    def load_contents(self, init_func=None, update_func=None, end_func=None):
        """
        Parses session history file, line by line and populates the history message on memory.
        """
        if not self.filepath: return

        nrows = csv.reader.count_metadata_rows(self.filepath)
        
        with open(self.filepath) as filestream:
            self.data = pd.read_csv(filestream, 
                delimiter=csv.CSV_DELIMITER, 
                quotechar=csv.CSV_QUOTECHAR, 
                quoting=csv.CSV_QUOTING,
                lineterminator=csv.CSV_LINETERMINATOR,
                skiprows=nrows
            )

        res = self.data.query("MSG=='{0}'".format(Session.INFO_SESSION_ENDED) )
        for index, row in res.iterrows():
            self.ended = dateutil.parser.parse(row['+INFO'])

    def load_info(self):
        if not self.filepath: return

        with open(self.filepath) as filestream:
            
            csvreader = csv.reader(filestream)

            self.subjects = []

            count = 0
            for row in csvreader:
                msg = BpodMessageParser.fromlist(row)

                if msg:
                    if isinstance(msg, SessionInfo):
                        if   msg.infoname==Session.INFO_PROTOCOL_NAME:
                            self.task_name = msg.infovalue

                        elif msg.infoname==Session.INFO_CREATOR_NAME:
                            self.creator = msg.infovalue
                        
                        elif msg.infoname==Session.INFO_SESSION_STARTED:
                            self.started = dateutil.parser.parse(msg.infovalue)

                        elif msg.infoname==Session.INFO_SESSION_ENDED:
                            self.ended = dateutil.parser.parse(msg.infovalue)

                        elif msg.infoname==Session.INFO_SERIAL_PORT:
                            self.board_serial_port = msg.infovalue

                        elif msg.infoname==Session.INFO_BOARD_NAME:
                            self.board_name = msg.infovalue

                        elif msg.infoname==Session.INFO_SETUP_NAME:
                            self.setup_name = msg.infovalue

                        elif msg.infoname==Session.INFO_SUBJECT_NAME:
                            self.subjects += [ msg.infovalue ]
                            name, uuid4 = eval(msg.infovalue)
                            subj = self.project.find_subject_by_id(uuid4)
                            if subj is not None:
                                subj += self
                    else:
                        count += 1

                if count>50: break
    
    