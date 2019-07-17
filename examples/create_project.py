from pybpodgui_api.models.project import Project

# create the project
proj = Project()
proj.name = 'First project'

# add an experiment to the project
exp = proj.create_experiment()
exp.name = 'First experiment'

# add a setup to the project
stp = exp.create_setup()
stp.name = 'First setup'

# add a board to the project
board = proj.create_board()
board.name = 'First board'
board.serial_port = 'COM3'

# add subjects to the project
subj = proj.create_subject()
subj.name = 'First animal'

subj2 = proj.create_subject()
subj2.name = 'Second animal'

# add a new task\protocol to the project
task = proj.create_task()
task.name = 'First task'

exp.task = task         # set the task\protocol to the experiment
stp.board = board       # set the board to the setup
stp += [subj, subj2]    # add a subject to the setup

proj.save('my-project-folder')

task.code = 'print("My first protocol")'

proj.save(proj.path)
