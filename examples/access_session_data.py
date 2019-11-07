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
            # Do somehting
        elif msg.check_type('stderr'):
            pass
            # Do something
