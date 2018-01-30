#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re

version = ''
with open('pybpodgui_api/__init__.py', 'r') as fd: version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                                                                      fd.read(), re.MULTILINE).group(1)
if not version: raise RuntimeError('Cannot find version information')

requirements = [
	'pysettings>=1.0.0',
	'pyserial>= 3.1.1',
	'logging-bootstrap>=1.0.0',
]

setup(
	name='pybpod-gui-api',
	version=version,
	description="""ppybpod-gui-api is an API for the PyBpodGUI""",
	author=['Ricardo Ribeiro', 'Carlos Mão de Ferro'],
	author_email='ricardojvr@gmail.com',
	license='Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>',
	url='https://bitbucket.org/fchampalimaud/pycontrolgui',

	include_package_data=True,
	packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples', 'deploy', 'reports']),

)