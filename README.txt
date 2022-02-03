WELCOME TO THE PROCESS OF SETTING UP THIS WEBSERVER.

Requirements:
1. Python
2. Pip
3. Being able to setup a virtual environment
4. mySQL with the workbench
5. Creating a root user in the mySQL workbench or any other way (fully setup the root user)
6. This project was setup running in Windows Powershell

Setup:
1. Start by first creating the virtual environment (This link will help: https://pypi.org/project/virtualenv/)
2. Copy the entire folder into the virtual environment location
3. Once the contents of the entire folder is in there, we can start using pip in the virtual environment
4. First, make sure that you have activated the virtual environment in most cases or at least in Powershell,
this means first going into the directory of where the virtual environment is located. If the virtual environment
was created successfully, then we can the command ".\Scripts\activate". You will know this connection was 
successful, if next to where it tells you the directory before that, you will see
"(virtualenvironment_name) PS virtualenvironment_path>". 
5. Note that to leave the virtual environment at any time, make sure you are still located in the base path 
for the virtual environment, and you will just have to type "deactivate" in Powershell.
6. Now we need to use pip, to install the necessary modules. We will start by doing "python3 -m pip install Flask"
7. Now we will use to install the mysql library for python, type "python3 -m pip install mysql-connector-python" 
into Powershell
8. Now make sure you have downloaded mySQL and set it up with a base root user, the root password can be anything.
WARNING: WE WILL BE USING ROOT USER FOR THE DATABASE, KEEP THIS IN MIND, WHICH IS WHY WE USE A VIRTUAL ENVIRONMENT.
9. Now we need to install the other library for creating the plot to do this type "python3 -m pip install matplotlib".
10. So everything, should be setup to start running some python scripts. To intialize the database, we can simply
run a the script called "intializeDatabase.py", which will require you to input your root user password from the 
mysql step. This script will setup the initial database. 
11. Now you can open the mySQL workbench and you should see when you connect to root user, that there is a new schema,
called covidTest, there should be three tables called counties, states, population. If these have been populated then you 
can move on to the next step, otherwise delete the schema, and rerun the script from step 10.
12. Now that the database is setup, we need to do one more thing before we can run the web server. Finally, go into the
"app.py" file, and change the global variable called "PASSWORD" it is currently set to "CHANGE THIS PASSWORD". Change this
to your mySQL root password. You can now run the python file app.py. 

NOTE: Since we did a pip install using python3, make sure that you run any python files doing python3 fileName.
