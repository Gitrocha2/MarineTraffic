# Flask RestAPI

## Requirements

* Python 3
* Windows* (only if want to use configuration script automation)

## Quickstart

In the first use, at Admin privileges powershell, you need to execute the commands:

```shell
$ cd <YourPath>/RestAPI
$ cmd.exe /c 'installvenvs.bat'
```

After that all dependencies will be installed and python up-to-date. For the further runs, there is no need to install
dependencies in virtual enviroment again.


Finally, to start application run "startlocal.bat" or execute the following command:

```shell
$ env\Scripts\activate && python Main/startapp.py runserver --host 127.0.0.1 --port 5000
```

## Endpoints

To read application logs go to:

* http://127.0.0.1:5000/log

To post new employee information to database, send a json in the format of {"name": "Rachel Higgs", "age": 18, "role": "Trainee"} to the folowing endpoint:

* http://127.0.0.1:5000/new-employees
---
To delete employee information from database, send a json in the format of {"id":9} to the folowing endpoint:

* http://127.0.0.1:5000/employees
---
To updade employee information of database, send a json in the format of {"id": 1, "role": "Manager"} to the folowing endpoint:

* http://127.0.0.1:5000/employees
---
To get employee information from database, query using parameters in the following format:

* http://127.0.0.1:5000/employees?name=Justin%20Tau
---
Or, to get employee information by id, use the given format using url parameter:

*http://127.0.0.1:5000/employees-by-id?id=1


## Database

All data is stored in a database file (Employees.db) located at folder Main/database/data and after starting application first time it will be configured.

Further development is necessary to persist information in a cloud service database.


---
---

> 
> WARNING  
> Keep the requirements.txt updated by the following command:  
> pipenv lock -r > requirements.txt
> 
