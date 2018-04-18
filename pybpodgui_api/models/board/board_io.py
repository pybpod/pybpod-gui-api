# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging
import pybpodgui_api
from pybpodgui_api.models.board.board_base import BoardBase
from sca.formats import json


logger = logging.getLogger(__name__)


class BoardIO(BoardBase):
    """
    
    """

    def __init__(self, project):
        super(BoardIO, self).__init__(project)

        # repository that will manage the project files
        self.repository = None

    
    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'serial_port': self.serial_port})

        return data

    def save(self, parent_repository):
        """
        Save experiment data on filesystem.

        :ivar dict parent_path: Project path.  
        :return: Dictionary containing the board info to save. If None is returned, it means that ther was a failure.   
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping board without name")
            return None
        else:

            # if the project was loaded then it will reuse the repository otherwise create a new repository ################################
            repository = self.repository = self.repository if self.repository else parent_repository.sub_repository(self.name, uuid4=self.uuid4)
            ################################################################################################################################

            repository.uuid4    = self.uuid4
            repository.software = 'PyBpod GUI API v'+str(pybpodgui_api.__version__)
            repository.def_url  = 'http://pybpod.readthedocs.org'
            repository.def_text = 'This file contains the configuration of Bpod board.'
            repository.name     = self.name
            
            repository['serial-port']           = self.serial_port
            repository['enabled-bncports']      = self.enabled_bncports
            repository['enabled-wiredports']    = self.enabled_wiredports
            repository['enabled-behaviorports'] = self.enabled_behaviorports
            repository['net-port']              = self.net_port
            
            repository.commit()
            
            return repository

    def load(self, repository):
        """
        Load board data from filesystem

        :ivar str board_path: Path of the board
        :ivar dict data: data object that contains all board info
        """
        self.repository = repository
        
        self.uuid4                  = repository.uuid4 if repository.uuid4 else self.uuid4
        self.name                   = repository.name
        self.serial_port            = repository.get('serial-port',           repository.get('serial_port', None) )
        self.enabled_bncports       = repository.get('enabled-bncports',      None)
        self.enabled_wiredports     = repository.get('enabled-wiredports',    None)
        self.enabled_behaviorports  = repository.get('enabled-behaviorports', None)
        self.net_port  = repository.get('net-port', None)


    def __generate_boards_path(self, project_path):
        return os.path.join(project_path, 'boards')

    def __generate_board_path(self, boards_path):
        return os.path.join(boards_path, self.name)