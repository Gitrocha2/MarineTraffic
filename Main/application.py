from flask import Flask
from flask_restful import Api
import log
import features
from database import configdb
from flask_cors import CORS


def base_app():

    """
    Initialize application and add resources to interact with employees Database
    """
    print(' * Initializing API.')
    restapi = Flask(__name__)
    CORS(restapi, supports_credentials=False)
    log.start()
    api = Api(restapi)
    # Employees resources
    #api.add_resource(features.EmployeesResource1, '/employees')
    #api.add_resource(features.EmployeesResource2, '/employees-by-id')
    #api.add_resource(features.EmployeesResource3, '/employees-like')
    #api.add_resource(features.EmployeesResource4, '/employees-roles')
    #api.add_resource(features.NewEmployeesResource, '/new-employees')
    # Logs visualization
    api.add_resource(features.LogResource, '/log')

    # Front mocking
    #api.add_resource(features.FrontMock, '/run')

    # Create Database
    configdb.start_database()

    return restapi
