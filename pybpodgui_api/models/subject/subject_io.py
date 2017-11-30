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

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    
    def save(self, repository):
        """
        Save subject data on filesystem.

        :ivar str project_path: Project path.  
        :return: Dictionary containing the setup info to save.  
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping subject without name")
        else:

            repository.uuid4    = self.uuid4
            repository.software = 'PyBpod GUI API v'+str(pybpodgui_api.__version__)
            repository.def_url  = 'http://pybpod.readthedocs.org'
            repository.def_text = 'This file contains information about a subject used on PyBpod GUI.'
            repository['name']  = self.name

            repository.add_parent_ref(self.project.uuid4)

            self.path = repository.save()
            
            return repository

    def load(self, repository):
        """
        Load sebject data from filesystem

        :ivar str subject_path: Path of the subject
        :ivar dict data: data object that contains all subject info
        """
        self.uuid4= repository.uuid4 if repository.uuid4 else self.uuid4
        self.name = repository.get('name', None)