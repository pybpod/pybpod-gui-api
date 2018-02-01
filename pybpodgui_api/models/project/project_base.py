# !/usr/bin/python3
# -*- coding: utf-8 -*-

""" pycontrol.api.models.project

"""
import logging, uuid
from pybpodgui_api.models.experiment import Experiment
from pybpodgui_api.models.board      import Board
from pybpodgui_api.models.task       import Task
from pybpodgui_api.models.subject    import Subject


logger = logging.getLogger(__name__)


class ProjectBase(object):
    """
    A project is a collection of experiments and an hardware configuration
    """

    def __init__(self):
        self.uuid4      = uuid.uuid4()
        self.name           = ''
        self._experiments   = []
        self._tasks         = []
        self._boards        = []
        self._subjects      = []
        self._path          = None

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def subjects(self):
        """
        Get the list of subjects in the project

        :rtype: list(Subject)
        """
        return self._subjects

    @property
    def experiments(self):
        """
        Get the list of experiments in the project

        :rtype: list(Experiment)
        """
        return self._experiments

    @property
    def boards(self):
        """
        Get the list of boards in the project

        :rtype: list(Board)
        """
        return self._boards

    @property
    def tasks(self):
        """
        Get the list of tasks in the project

        :rtype: list(Task)
        """
        return self._tasks

    @property
    def path(self):
        """
        Get and set the project path

        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def name(self):
        """
        Get and set the project name

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def __add__(self, obj):     
        if isinstance(obj, Experiment): self._experiments.append(obj)
        if isinstance(obj, Board):      self._boards.append(obj)
        if isinstance(obj, Task):       self._tasks.append(obj)
        if isinstance(obj, Subject):    self._subjects.append(obj)
        return self

    def __sub__(self, obj):
        if isinstance(obj, Experiment): self._experiments.remove(obj)
        if isinstance(obj, Board):      self._boards.remove(obj)
        if isinstance(obj, Task):       self._tasks.remove(obj)
        if isinstance(obj, Subject):    self._subjects.remove(obj)
        return self

    def find_board(self, name):
        """
        Find a board by the name

        :ivar str name: Name of the board to find.
        :rtype: Board
        """
        for board in self.boards:
            if board.name == name: return board
        return None

    def find_task(self, name):
        """
        Find a task by the name

        :ivar str name: Name of the task to find.
        :rtype: Task
        """
        for task in self.tasks:
            if task.name == name: return task
        return None

    def find_subject(self, name):
        """
        Find a subject by the name

        :ivar str name: Name of the subject to find.
        :rtype: Subject
        """
        for subject in self.subjects:
            if subject.name == name: return subject
        return None

    def create_experiment(self):
        """
        Add an experiment to the project, and return it.
        
        :rtype: Experiment
        """
        return Experiment(self)

    def create_board(self):
        """
        Add an board to the project, and return it.
        
        :rtype: Board
        """
        return Board(self)

    def create_task(self):
        """
        Add an task to the project, and return it.
        
        :rtype: Task
        """
        return Task(self)

    def create_subject(self):
        """
        Add an subject to the project, and return it.
        
        :rtype: Subject
        """
        return Subject(self)
