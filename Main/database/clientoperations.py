from database import entities
#from entities import entities.Employee
#from connectors import add_employee, find_employee_exact, \
#    find_employee_close, update_age, remove_employee
from database import connectors
import sqlite3


def client_test():

    #conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('./Main/database/data/Employees.db')

    emp_1 = entities.Employee('John Gluon', 30, 'Developer')
    connectors.add_employee(emp_1, conn)
    emp_2 = entities.Employee('Mary Boson', 36, 'Human Resources')
    connectors.add_employee(emp_2, conn)
    emp_3 = entities.Employee('Justin Tau', 27, 'Project Manager')
    connectors.add_employee(emp_3, conn)
    emp_4 = entities.Employee('Rachel Higgs', 18, 'Trainee')
    connectors.add_employee(emp_4, conn)
    emp_5 = entities.Employee('John Charm', 20, 'Salesman')
    connectors.add_employee(emp_5, conn)

    query1 = connectors.find_employee_exact('John Gluon', conn)
    #print('Query1, Find entities.Employee named John Gluon....', query1)

    query1b = connectors.find_employee_close('Mary', conn)
    #print('Query1b, Find entities.Employee named Mary....', query1b)

    connectors.update_role('Mary Boson', 'HR Manager', conn)
    query2 = connectors.find_employee_close('Mary', conn)
    #print('Query2, after update Mary age, it becomes... ', query2)

    query3 = connectors.find_employee_close('John', conn)
    #print('Query3, Find all employees named John...', query3)

    connectors.remove_employee(4, conn)
    query4 = connectors.find_employee_exact('Rachel Higgs', conn)
    #print('Query4 ', query4)

    emp_6 = entities.Employee('Mark Neutrino', 28, 'Analyst')
    connectors.add_employee(emp_6, conn)

    conn.close()

    return {'Status': 'ok'}
