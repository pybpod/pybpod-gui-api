# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os, uuid
from .other_taskfile import OtherTaskFile
from pybpodgui_api.utils.send2trash_wrapper import send2trash

logger = logging.getLogger(__name__)

class TaskBase(object):
    """ Represents a state machine """

    def __init__(self, project=None):
        """
        :ivar Project project: Project to which the Task belongs to.
        """
        self.uuid4   = uuid.uuid4()
        self.name    = 'Untitled task {0}'.format( len(project.tasks) ) if project else None
        self.project = project
        self.project += self
        self.trigger_softcodes = False
        
        self.filepath = None

        self._otherfiles = []
        
    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def name(self): 
        """
        Get and set task name

        :rtype: str
        """
        return self._name
       
    @name.setter
    def name(self, value): self._name = value

    @property
    def path(self): 
        """
        Get and set task path

        :rtype: str
        """
        if self.project.path is None: return None
        return os.path.join(self.project.path, 'tasks', self.name)

    @property
    def filepath(self):
        """
        Get and set task file path

        :rtype: str
        """
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

    
    @property
    def project(self):          
        """
        Get and set project

        :rtype: Project
        """        
        return self._project
    @project.setter
    def project(self, project): self._project = project

    @property
    def otherfiles(self):          
        """
        Get and set project

        :rtype: Project
        """        
        return self._otherfiles
    @otherfiles.setter
    def otherfiles(self, value): self._otherfiles = value

    @property
    def trigger_softcodes(self):
        """
        Get net port

        :rtype: int
        """
        return self._trigger_softcodes

    @trigger_softcodes.setter
    def trigger_softcodes(self, value):
        self._trigger_softcodes = value


    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def create_otherfile(self):
        """
        Add a other file to a task and return it.
        
        :rtype: Experiment
        """
        return OtherTaskFile(self)

    def __add__(self, obj):     
        if isinstance(obj, OtherTaskFile): self._otherfiles.append(obj)
        return self

    def __sub__(self, obj):
        if isinstance(obj, OtherTaskFile): self._otherfiles.remove(obj)
        return self



    def remove(self):
        """
        Remove the task from the project.
        """
        pass
    
    def __unicode__(self):  return self.name
    def __str__(self):      return self.__unicode__()
