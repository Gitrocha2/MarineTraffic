from flask_script import Server, Manager
from application import base_app
import log
from flask_cors import CORS


manager = Manager(base_app())
manager.add_command('runserver', Server(use_debugger=False, use_reloader=False, threaded=True))

if __name__ == '__main__':
    """
    Run Flask server in given host and port in the format 
    python Main/startapp.py runserver --host X.Y.Z.W --port N
    """
    CORS(base_app(), supports_credentials=False)
    log.info('Application has started.')
    manager.run()
