# !/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class TaskVariable(object):
	def __init__(self, name, value=None, persistent=False):
		self.name = name
		self.value = value
		self.persistent = persistent

	@property
	def name(self): return self._name

	@name.setter
	def name(self, value): self._name = value

	@property
	def value(self): return self._value

	@value.setter
	def value(self, value): self._value = value

	@property
	def persistent(self): return self._persistent

	@persistent.setter
	def persistent(self, value):  self._persistent = value

	def collect_data(self, data):
		data.update({'name': str(self.name)})
		data.update({'value': self.value})
		data.update({'persistent': str(self.persistent)})

		return data

	def save(self):
		data2save = {}
		data2save.update({'name': str(self.name)})
		data2save.update({'value': self.value})
		data2save.update({'persistent': str(self.persistent)})

		return data2save

	def load(self, setup_path, data):
		self.name = data['name']
		self.value = data['value']
		self.persistent = data['persistent']
