# To-Do_app

This project uses node, npm, python and flask. Go to check out If you don't have them locally installed.

frontend:
This project using node and npm in frontend, when you running this project please check the enviroments.

install node.js from this website:
https://nodejs.org/en/

and npm, run below code in your terminal:
$ sudo npm install npm --global // Update thenpmCLI client

install angular mui:

$ ng add @angular/material

if you wanna run frontend using
$ ng serve --open


backend:
This project using python 3.7 and pip3, when you running this project please check the enviroment.

install requirements using:
Go to backend and running below code in your terminal.

$ cd To-Do_app/todoapp/backend

$ pip install -r requirements.txt

to make sure you can get data from data base, please install google-cloud-sql:

$ python3 -m pip install cloud-sql-python-connector==0.9.3

if you wanna run backend using 
$ python app.py


When you want to access google-cloud-sql, the detail is include in DbConnector.py
instance_connection_name = "to-do-app-378206:us-central1:todoappdb"  
db_user = "postgres"  
db_password = "zuqiangyu123"  
db_name = "postgres"  


