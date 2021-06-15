# Web Application (Python 3+ Pandas)

## Case overview

This project create a application to query and analyze Marine Traffic information. The backend is using python 3+ and pandas.

## Structure

This project in the future will be divided in two parts:

* ### ` Backend: Using Python and Flask`

At 'Main' folder, the backend structure can be accessed and all project files, included local database (SQLite3).

* ### ` Front-End: Using ReactJS`

At 'Front-React' folder, the front-end project can be viewed.

## Quickstart

* ### ` In the first use, click in "installvenvs.bat"`
* ### `And, for next uses, just start it by clicking in "start-query.bat"`
* ### `or clicking in "start-analysis.bat"`

## Basic usage


You can use the application to check for individuals ships, fleets of ships or periods of time.

#### Individual
For individual query, when app starts, choose "IMO" and type the number of the ship. The trips and cargo history will be
 inside folder "Reports" called "IMO-{number}"
 
#### Fleets
For fleets analysis, choose "ARQUIVO" instead and then the result will show inside Folder "Reports/Fleets" organized by groups.
You need to fill the file inside "Inputs" folder called "fleets.txt". The correct format for organizing is:

    Group-name-1;IMO-number-1,IMO-number-2,...
    Group-name-2;IMO-number-3,IMO-number-4,...
    
##### Example:
    Big-Tankers;9453858,9453834
    Small-Tankers;8617079

#### Period
For period of time analysis choose "Estudo". The type the years comma separated (Example: 2019,2018,2017). From 2010 till 2019.
The result will be in folder "Reports/Research"

#### Analysis
After querying ships information you can choose option "ANALISE", to analyze all the history data.


## Comments

You'll need to download required file listed in instructions to test it locally.

>For further instructions check the README files in botch folders and proceed to >installation of the project in the first run.
