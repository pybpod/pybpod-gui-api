# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A board represents the hardware that controls the running session for a specific setup.
"""

import os, uuid
import logging
logger = logging.getLogger(__name__)


class BoardBase(object):
    """
    Board base class with main attributes. A board should have a name, serial port, project belonging to, a path and a list of messages.
    """

    def __init__(self, project):
        """
        :ivar Project project: Project to which the Board belongs to.
        """
        self.uuid4      = uuid.uuid4()
        
        self.name = 'Untitled box {0}'.format(len(project.boards))
        self.serial_port = None
        self.project = project

        self._path = None
        self.log_messages = []

        self.project += self

        self.enabled_bncports       = None
        self.enabled_wiredports     = None
        self.enabled_behaviorports  = None

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def name(self):
        """
        Get and set the board name

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def serial_port(self):
        """
        Get and set the board serial port

        :rtype: str
        """
        return self._serial_port

    @serial_port.setter
    def serial_port(self, serial_port):
        self._serial_port = serial_port

    @property
    def project(self):
        """
        Get and set the board project

        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, value):
        self._project = value


    @property
    def path(self):
        """
        Get and set the board path

        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def enabled_bncports(self):
        """
        Get and set enabled bncports

        :rtype: list(Boolean)
        """
        return self._enabled_bncports

    @enabled_bncports.setter
    def enabled_bncports(self, value):      self._enabled_bncports = value

    @property
    def enabled_wiredports(self):
        """
        Get and set the enabled wired ports

        :rtype: list(Boolean)
        """
        return self._enabled_wiredports

    @enabled_wiredports.setter
    def enabled_wiredports(self, value): self._enabled_wiredports = value

    @property
    def enabled_behaviorports(self):
        """
        Get and set the experiment name

        :rtype: list(Boolean)
        """
        return self._enabled_behaviorports

    @enabled_behaviorports.setter
    def enabled_behaviorports(self, value): self._enabled_behaviorports = value

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def remove(self):
        pass

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


