# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging, pybpodgui_api
from pybpodgui_api.models.subject.subject_base import SubjectBase

from sca.formats import json

logger = logging.getLogger(__name__)


class SubjectIO(SubjectBase):
    """
    
    """

    def __init__(self, project):
        super(SubjectIO, self).__init__(project)

        # repository that will manage the project files
        self.repository = None


    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    
    def save(self, parent_repository):
        """
        Save subject data on filesystem.

        :ivar str project_path: Project path.  
        :return: Dictionary containing the setup info to save.  
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping subject without name")
            return None
        else:
            # if the project was loaded then it will reuse the repository otherwise create a new repository ################################
            repository = self.repository = self.repository if self.repository else parent_repository.sub_repository('subjects', self.name, uuid4=self.uuid4)
            ################################################################################################################################

            repository.uuid4    = self.uuid4
            repository.software = 'PyBpod GUI API v'+str(pybpodgui_api.__version__)
            repository.def_url  = 'http://pybpod.readthedocs.org'
            repository.def_text = 'This file contains information about a subject used on PyBpod GUI.'
            repository.name     = self.name
            
            repository.commit()

            return repository

    def load(self, repository):
        """
        Load sebject data from filesystem

        :ivar str subject_path: Path of the subject
        :ivar dict data: data object that contains all subject info
        """
        self.repository = repository

        self.uuid4 = repository.uuid4 if repository.uuid4 else self.uuid4
        self.name  = repository.name