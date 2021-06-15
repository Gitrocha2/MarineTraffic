from flask import Response, stream_with_context, current_app, make_response, render_template, Flask, request
from flask_restful import Resource, Api
import log
import sys
from database import connectors
import sqlite3
from database import entities


# Main methods for interact with db
class EmployeesResource1(Resource):
    """
    Create class methods of API - Get, Post, Delete and Update
    """

    def get(self):

        try:
            employee_name = request.args.get('name', default=0, type=str)

            conn = sqlite3.connect('./Main/database/data/Employees.db')
            result = connectors.find_employee_exact(empname=employee_name, connection=conn)
            conn.close()
            string = f'User queried for employee {employee_name}'

            log.info(string)

        except:
            log.info(f'Failed to find employee')
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            log.info(errormsg)

            result = {'Status': 'error', 'Message': errormsg}

        return result

    def delete(self):

        try:
            employee_id = request.get_json()['id']

            conn = sqlite3.connect('./Main/database/data/Employees.db')
            result = connectors.remove_employee(employeeid=int(employee_id), connection=conn)
            conn.close()
            string = f'User deleted employee {employee_id} info from database.'

            log.info(string)

        except:
            log.info("Could not delete employee info from database.")
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            log.info(errormsg)

            result = {'Status': 'error', 'Message': errormsg}

        return result

    def put(self):

        try:
            employee = request.get_json()
            employee_id = employee['id']
            employee_role = employee['role']

            conn = sqlite3.connect('./Main/database/data/Employees.db')
            result = connectors.update_role(employeeid=employee_id, newrole=employee_role, connection=conn)
            conn.close()

            string = f'User updated employee {employee_id} role in database.'
            log.info(string)

        except:
            log.info("Could not update employee role in database.")
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            log.info(errormsg)
            result = {'Status': 'error', 'Message': errormsg}

        return result


# Find employees by exact ID
class EmployeesResource2(Resource):
    """
    Create class methods of API - Get by ID
    """

    def get(self):

        try:
            employee_id = request.args.get('id', default=0, type=int)

            conn = sqlite3.connect('./Main/database/data/Employees.db')
            result = connectors.find_employee_exactid(empid=employee_id, connection=conn)
            conn.close()
            string = f'User queried for employee id {employee_id}'

            log.info(string)

        except:
            log.info(f'Failed to find employee')
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            log.info(errormsg)

            result = {'Status': 'error', 'Message': errormsg}

        return result


# Find all employees named like inputs
class EmployeesResource3(Resource):
    """
    Create class methods of API - Get by ID
    """

    def get(self):

        try:
            employee_name = request.args.get('name', default='', type=str)

            conn = sqlite3.connect('./Main/database/data/Employees.db')
            result = connectors.find_employee_close(namelike=employee_name, connection=conn)
            conn.close()
            string = f'User queried for employee name like {employee_name}'

            log.info(string)

        except:
            log.info(f'Failed to find employee')
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            log.info(errormsg)

            result = {'Status': 'error', 'Message': errormsg}

        return result


# Find all employees roles like inputs
class EmployeesResource4(Resource):
    """
    Create class methods of API - Get by ID
    """

    def get(self):

        try:
            employee_role = request.args.get('role', default='', type=str)

            conn = sqlite3.connect('./Main/database/data/Employees.db')
            result = connectors.find_employee_roles(rolelike=employee_role, connection=conn)
            conn.close()
            string = f'User queried for employee role like {employee_role}'

            log.info(string)

        except:
            log.info(f'Failed to find employee')
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            log.info(errormsg)

            result = {'Status': 'error', 'Message': errormsg}

        return result


# Methods for new employee register
class NewEmployeesResource(Resource):
    """
    Create class methods of API - Post new employee to database
    """

    def post(self):

        try:
            employee = request.get_json()
            #print(employee)
            #print(employee['name'])
            new_emp = entities.Employee(employee['name'], employee['age'], employee['newrole'])

            conn = sqlite3.connect('./Main/database/data/Employees.db')
            result = connectors.add_employee(employee=new_emp, connection=conn)
            conn.close()

            string = f'User added new employee in database. - Name: {new_emp.name}, position: {new_emp.role}'
            log.info(string)

        except:
            log.info("Could not post information.")
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            log.info(errormsg)
            result = {'Status': 'error', 'Message': errormsg}

        return result


#Query log by get
class LogResource(Resource):

    def get(self):

        try:
            syslog = open('log/syslog.log', 'r')
        except:
            log.info("Faile to open log file")
            return 'no log file found'
        content = stream_with_context(syslog)
        response = Response(content)
        response.headers['Content-type'] = 'text/plain'

        return response


# Class for mass DB data insert
class FrontMock(Resource):

    def get(self):

        try:
            from database import clientoperations
            result = clientoperations.client_test()

        except:
            log.info("Could not post information")
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])

            log.info(errormsg)
            result = {'Status': 'error', 'Message': errormsg}

        return result
