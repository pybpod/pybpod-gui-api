#!/usr/bin/python
# -*- coding: utf-8 -*-

""" src.api.util """

__author__ = "Carlos Mao de Ferro"
__copyright__ = ""
__credits__ = "Carlos Mao de Ferro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mao de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


def makeLambdaFunc(func, **kwargs):
    """ Auxiliar function for passing parameters to functions """
    return lambda: func(**kwargs)


class DotDict(object):

    def __init__(self, **kwds):
        self.__dict__.update(kwds)


def __main__():
    pass
