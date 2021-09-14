'''
Module functions to properly interact with Database
'''
import sqlite3


def add_data(atr, connection):

    with connection:
        c = connection.cursor()
        c.execute("INSERT INTO tempos_atr_2019 (IDAtracacao,"
                  "TEsperaAtracacao,"
                  "TEsperaInicioOp,"
                  "TOperacao,"
                  "TEsperaDesatracacao,"
                  "TAtracado,"
                  "TEstadia) VALUES (:idatr, :tespatr, :tespin, :top, :tespout, :ttot, :testad)",
                  {'idatr': atr['idatr'],
                   'tespatr': atr['tespatr'],
                   'tespin': atr['tespin'],
                   'top': atr['top'],
                   'tespout': atr['tespout'],
                   'ttot': atr['ttot'],
                   'testad': atr['testad']})

    return {'Status': 'ok'}


def find_atr_exact(atrid, connection):

    c = connection.cursor()
    c.execute("SELECT * FROM atrstats WHERE IDAtracacao=:AtrID", {'AtrID': atrid})

    result = c.fetchall()

    if len(result) == 0:
        message = f'Employee {atrid} not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def find_imo_exact(imo, connection):

    c = connection.cursor()
    c.execute("SELECT * FROM atrstats WHERE [NdoIMO]=:NIMO", {'NIMO': imo})

    result = c.fetchall()

    if len(result) == 0:
        message = f'Ship {imo} not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def find_trips_mmyyyy(month, year, connection):

    c = connection.cursor()

    datestring = f'___{month}/{year}'

    c.execute(f"SELECT * FROM atrstats WHERE [Data Chegada] LIKE '{datestring}%' ORDER BY [DataChegada]")

    result = c.fetchall()

    # No ship found
    if len(result) == 0:
        message = f'Ship not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def find_ships_by_trips(imolist, connection):

    c = connection.cursor()
    atrid = ", ".join(map(str, imolist))
    query = f"SELECT * FROM atrstats WHERE IDAtracacao IN ({atrid})"
    c.execute(query)

    result = c.fetchall()

    if len(result) == 0:
        message = f'Load ID {atrid} not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def find_imolist_exact(imolist, connection):


    '''
    loadid = ", ".join(map(str, loadid))
    query = f"SELECT * FROM loadsinfo WHERE IDAtracacao IN ({loadid})"
    :param imolist:
    :param connection:
    :return:
    '''

    #imolist = ", ".join(map(str, imolist))
    c = connection.cursor()
    c.execute(f"SELECT * FROM atrstats WHERE [NdoIMO] IN ({imolist})")

    result = c.fetchall()

    # No ship found
    if len(result) == 0:
        message = f'Ship not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def find_load_exact(loadid, connection):

    c = connection.cursor()
    loadid = ", ".join(map(str, loadid))
    query = f"SELECT * FROM loadsinfo WHERE IDAtracacao IN ({loadid})"
    c.execute(query)

    result = c.fetchall()

    if len(result) == 0:
        message = f'Load ID {loadid} not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def find_port_atr(atrid, connection):

    c = connection.cursor()
    loadid = ", ".join(map(str, loadid))
    query = f"SELECT * FROM loadsinfo WHERE IDAtracacao IN ({loadid})"
    c.execute(query)

    result = c.fetchall()

    if len(result) == 0:
        message = f'Load ID {loadid} not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def find_port_loads(portid, connection):

    c = connection.cursor()

    '''
    "SELECT * FROM atrstats WHERE IDAtracacao=:AtrID", {'AtrID': atrid}
    Destino=:PortID
    '''
    query = f"SELECT * FROM loadsinfo WHERE Origem=:PortID " \
        f"UNION " \
        f"SELECT * FROM loadsinfo WHERE dESTINO=:PortID"

    c.execute(query, {'PortID': portid})

    result = c.fetchall()

    if len(result) == 0:
        message = f'Load ID {portid} not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}

#print(find_load_exact([900859, 941672], connection=sqlite3.connect('./Main/database/data/atr_info.db')))


def find_imo_blank(connection):

    c = connection.cursor()
    c.execute("SELECT * FROM atrstats WHERE [NdoIMO] IS NULL "
              "OR [NdoIMO] = 0 "
              "OR [NdoIMO] = ' ' "
              "OR TRIM([NdoIMO]) = ''")

    #c.execute("SELECT * FROM atrstats")
    result = c.fetchall()

    if len(result) == 0:
        message = f'ShipS not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def count(connection):

    c = connection.cursor()
    #c.execute("SELECT * FROM atrstats WHERE [NdoIMO] IS NULL OR [NdoIMO] = 0 OR [NdoIMO] = ' ' ")
    c.execute("SELECT COUNT(*) FROM atrstats")
    result = c.fetchall()

    if len(result) == 0:
        message = f'ShipS not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def find_employee_close(namelike, connection):

    c = connection.cursor()
    likename = f'%{namelike}%'
    c.execute("SELECT * FROM employees_list WHERE name LIKE :name", {'name': likename})

    result = c.fetchall()

    if len(result) == 0:
        message = f'Employee name similar to {namelike} not found.'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def find_employee_roles(rolelike, connection):

    c = connection.cursor()
    likename = f'%{rolelike}%'
    c.execute("SELECT * FROM employees_list WHERE role LIKE :role", {'role': likename})

    result = c.fetchall()

    if len(result) == 0:
        message = f'Employee role similar to {rolelike} not found.'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def find_employee_exactid(empid, connection):

    c = connection.cursor()
    c.execute("SELECT * FROM employees_list WHERE id=:id", {'id': empid})

    result = c.fetchall()

    if len(result) == 0:
        message = f'Employee {empid} not found'
        result = {'Status': 'ok', 'Message': message}
        return result

    return {'Status': 'ok', 'Message': result}


def update_role(employeeid, newrole, connection):

    with connection:
        c = connection.cursor()

        c.execute("SELECT * FROM employees_list WHERE id=:id", {'id': employeeid})

        result = c.fetchall()

        if len(result) > 0:

            c.execute("""UPDATE employees_list SET role = :role
                        WHERE id = :id""",
                      {'id': employeeid, 'role': newrole})

            message = f'Employee {employeeid}, changed role to {newrole}.'

            return {'Status': 'ok', 'Message': message}

        message = f'There is no occurrence of id {employeeid}'

        return {'Status': 'error', 'Message': message}


def remove_employee(employeeid, connection):

    with connection:
        c = connection.cursor()
        c.execute("SELECT * FROM employees_list WHERE id=:id", {'id': employeeid})

        result = c.fetchall()

        if len(result) > 0:

            c.execute("DELETE from employees_list WHERE id = :id", {'id': employeeid})

            message = f'Removed employee ID: {employeeid} from database.'

            return {'Status': 'ok', 'Message': message}

        message = f'There is no occurrence of id {employeeid}'

        return {'Status': 'error', 'Message': message}


#conn = sqlite3.connect('./data/atr_info.db')
#print(find_trips_mmyyyy(month='01', year='2010', connection=conn))
