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

    
    def save(self, project_path):
        """
        Save subject data on filesystem.

        :ivar str project_path: Project path.  
        :return: Dictionary containing the setup info to save.  
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping subject without name")
        else:
            subjects_path = os.path.join(project_path, 'subjects')
            if not os.path.exists(subjects_path): os.makedirs(subjects_path)

            subject_path = os.path.join(subjects_path, self.name)
            if not os.path.exists(subject_path):  os.makedirs(subject_path)

            data2save = json.scadict(
                {'name': self.name},
                uuid4_id=self.uuid4,
                software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                def_url='http://pybpod.readthedocs.org',
                def_text='This file contains information about a subject used on PyBpod GUI.')

            data2save.add_parent_ref(self.project.uuid4)

            with open(os.path.join(subject_path, 'subject-settings.json'), 'w') as jsonfile:
                json.dump(data2save, jsonfile)
            
            self.path = subject_path

            return data2save

    def load(self, subject_path, data):
        """
        Load sebject data from filesystem

        :ivar str subject_path: Path of the subject
        :ivar dict data: data object that contains all subject info
        """

        with open(os.path.join(subject_path, 'subject-settings.json'), 'r') as jsonfile:
            data      = json.load(jsonfile)
            self.uuid4= data.uuid4 if data.uuid4 else self.uuid4
            self.name = data['name']