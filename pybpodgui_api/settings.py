# # !/usr/bin/python3
# # -*- coding: utf-8 -*-

import logging

# THESE SETTINGS ARE NEEDED FOR PYSETTINGS
APP_LOG_FILENAME = 'app.log'
APP_LOG_HANDLER_CONSOLE_LEVEL 	= logging.WARNING
APP_LOG_HANDLER_FILE_LEVEL 		= logging.WARNING

# BPOD GUI PLUGIN SETTINGS
APP_LOG_HANDLER_FILE_LEVEL 		= logging.WARNING
APP_LOG_HANDLER_CONSOLE_LEVEL 	= logging.WARNING


# [project], [experiment], [setup], [protocol], [datetime], [subjects]
PYBPODGUI_API_DEFAULT_SESSION_NAME = "[datetime]"