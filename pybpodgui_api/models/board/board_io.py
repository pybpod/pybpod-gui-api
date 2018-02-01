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
    
    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'serial_port': self.serial_port})

        return data

    def save(self, repository):
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
            repository.uuid4    = self.uuid4
            repository.software = 'PyBpod GUI API v'+str(pybpodgui_api.__version__)
            repository.def_url  = 'http://pybpod.readthedocs.org'
            repository.def_text = 'This file contains the configuration of Bpod board.'
            repository['name']          = self.name
            repository['serial_port']   = self.serial_port
            repository['enabled-bncports']      = self.enabled_bncports
            repository['enabled-wiredports']    = self.enabled_wiredports
            repository['enabled-behaviorports'] = self.enabled_behaviorports

            repository.add_parent_ref(self.project.uuid4)
            
            repository.save()

            self.name = repository.name

            return repository

    def load(self, repository):
        """
        Load board data from filesystem

        :ivar str board_path: Path of the board
        :ivar dict data: data object that contains all board info
        """
        self.uuid4                  = repository.uuid4 if repository.uuid4 else self.uuid4
        self.name                   = repository.name
        self.serial_port            = repository.get('serial_port',           None)
        self.enabled_bncports       = repository.get('enabled-bncports',      None)
        self.enabled_wiredports     = repository.get('enabled-wiredports',    None)
        self.enabled_behaviorports  = repository.get('enabled-behaviorports', None)


    def __generate_boards_path(self, project_path):
        return os.path.join(project_path, 'boards')

    def __generate_board_path(self, boards_path):
        return os.path.join(boards_path, self.name)