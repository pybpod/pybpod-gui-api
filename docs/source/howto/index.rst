.. _howto-label:


******************
Examples
******************


Create a new project
========================

Create a new project programmatically. The resulting project can be opened with the `PyBpod GUI <http://pybpod.readthedocs.io>`_.

.. code-block:: python
   
   from pybpodgui_api.models.project import Project

   # create the project
   proj = Project()
   proj.name = 'First project'

   # add an experiment to the project
   exp  = proj.create_experiment()
   exp.name = 'First experiment'

   # add a setup to the project
   stp  = exp.create_setup()
   stp.name = 'First setup'

   # add a board to the project
   board = proj.create_board()
   board.name = 'First board'
   board.serial_port = 'COM3'

   # add a subject to the project
   subj  = proj.create_subject()
   subj.name = 'First animal'

   # add a new task\protocol to the project
   task  = proj.create_task()
   task.name = 'First task'
   task.code = 'print("My first protocol")'

   exp.task  = task # set the task\protocol to the experiment
   stp.board = board # set the board to the setup
   stp += subj # add a subject to the setup

   proj.save('my-project-folder')


Access to data from a session
=============================

The next examples shows how to access the messages in a pybpod session.

.. code-block:: python
   
   from pybpodgui_api.models.project import Project

   # create the project
   proj = Project()
   proj.load('my-project-folder')

   exp = proj.experiments[0]
   stp = exp.setups[0]

   for session in stp.sessions:

      for msg in session.messages_history:

         if msg.check_type('INFO'):
            pass
            #Do somehting

         elif msg.check_type('stderr'):
            pass
            #Do something
