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

    def save(self, parent_path):
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
            # create the boards path if does not exist
            boards_path = self.__generate_boards_path(parent_path)
            if not os.path.exists(boards_path):
                os.makedirs(boards_path)

            # create the board path if does not exists
            board_path = self.__generate_board_path(boards_path)
            if not os.path.exists(board_path):
                os.makedirs(board_path)

            data2save = json.scadict({
                    'name':                     self.name,
                    'serial_port':              self.serial_port,
                    'enabled-bncports':         self.enabled_bncports,
                    'enabled-wiredports':       self.enabled_wiredports,
                    'enabled-behaviorports':    self.enabled_behaviorports,
                },
                uuid4_id=self.uuid4,
                software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                def_url ='http://pybpod.readthedocs.org',
                def_text='This file contains the configuration of Bpod board.'
            )
            data2save.add_parent_ref(self.project.uuid4)

            with open(os.path.join(board_path, 'board-settings.json'), 'w') as jsonfile:
                json.dump(data2save, jsonfile)

            self.path = board_path
            return data2save

    def load(self, board_path, data):
        """
        Load board data from filesystem

        :ivar str board_path: Path of the board
        :ivar dict data: data object that contains all board info
        """

        with open(os.path.join(board_path, 'board-settings.json'), 'r') as jsonfile:
            data = json.load(jsonfile)
            self.uuid4                  = data.uuid4 if data.uuid4 else self.uuid4
            self.name                   = data['name']
            self.serial_port            = data['serial_port']
            self.enabled_bncports       = data.get('enabled-bncports',      None)
            self.enabled_wiredports     = data.get('enabled-wiredports',    None)
            self.enabled_behaviorports  = data.get('enabled-behaviorports', None)

        self._path = board_path


    def __generate_boards_path(self, project_path):
        return os.path.join(project_path, 'boards')

    def __generate_board_path(self, boards_path):
        return os.path.join(boards_path, self.name)
