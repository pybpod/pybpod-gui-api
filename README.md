# PyBpod GUI API #

## Project information ##

This API makes available a set of functions and properties to allow the manipulation of a PyBpod GUI project using code.

This project is maintained by a team of SW developers at the Champalimaud Foundation.

## How to install ##

PyBpod's GUI API is available in PyPI. As such, in your Python environment you just need to:

`pip install pybpod-gui-api`

## Example ##

```python
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

    exp.task  = task # set the task\protocol to the experiment
    stp.board = board # set the board to the setup
    stp += subj # add a subject to the setup

    proj.save('my-project-folder')

    task.code = 'print("My first protocol")'

    proj.save(proj.path)
```

## Documentation ##

Documentation for this project can be found [here](https://pybpod.readthedocs.io/projects/pybpod-gui-api/)

## Parent project ##

PyBpod's website: [here](http://pybpod.com)

PyBpod's documentation: [here](https://pybpod.readthedocs.io)

## Feedback ##

Please use GitHub's issue system to submit feature suggestions, bug reports or to ask questions.
