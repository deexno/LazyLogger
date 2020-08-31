# LazyLogger - About
LazyLogger is a program that allows administrators to record who forgets to lock the screen and who does not. LazyLogger is system independent and works on MacOS, Windows and Linux. LazyLogger also has the advantage that it requiers nothing more than a database, that means LazyLogger can run completely without a domain controller and can also be installed on computers that are not available in a domain. LazyLogger also has the advantage that it works on Terminal Servers.

# Requirements
All you need is a database with MySQL version 5.5 or higher
(If you do not have a db, you can create a database completely free online on sites such as https://www.freemysqlhosting.net/)

# Installation

## Step 1.
First of all, it is important that you have Python 5.0 or higher installed on the system on which you want to install the program! This is the programming language in which the program was programmed and is fundamental for the following steps! Without Python the program will not work!

## Step 2.
<b><details><summary>For Windows-Systems</summary></b>

1. Once you have installed Python, download the project folder. After you have done this, I recommend moving it to "C:\Program Files\Python 3.8.3\" (this is optional but recommended so the program works properly)
  
2. Then execute the installation file (LazyLogger/installFiles/install_win.bat) This will install/update and prepare the required libaries.

3. Start the configurator (configurator.py) There, select the 1. Option. In this configurator you MUST now configure the database and make general settings.<br>
└> 3.1 Start the databasepreparer.py to prepare your database for the LazyLogger (It creates 2 tables which are needed)

4. Start the LazyLogger (LazyLogger.pyw)

5. And now finally put the LazyLogger.py and the logging.bat file into the autostart so that the LazyLogger is always running again after a System restart. Do not forget this step! (You can also start both scripts one after the other with only one script, this is up to you but I did this separately so that if you do this on a terminal server you only have to start logging.bat once you restart the terminal server)

<details><summary>5. For Windows-Terminal-Servers:</summary> 
If you want to set up LazyLogger on a terminal server do it like this:<br>
1. Put the logging.bat file in the terminal server autostart (so that when you restart the terminal server the LazyLogger will always work)<br>
2. Create a CPO under Policies/Windows Settings/Skripts which automatically starts the LazyLogger.py after a logon
</details>
</details>

<b><details><summary>For Linux & MacOS-Systems</summary></b>

1. Once you have installed Python, download the project folder. After you have done this, I recommend moving it to "/usr/bin/python/" (this is optional but recommended so the program works properly)
  
2. Then execute the installation file (LazyLogger/installFiles/install_linux.sh) This will install/update and prepare the required libaries.

3. Start the configurator (configurator.py) There, select the 1. Option. In this configurator you MUST now configure the database and make general settings.<br>
└> 3.1 Start the databasepreparer.py to prepare your database for the LazyLogger (It creates 2 tables which are needed)

4. Start the LazyLogger (LazyLogger.pyw)

5. And now finally create a crontab which will automatically start the LazyLogger. py and the logging. Sh script so that the LazyLogger is always running again after a System restart. Do not forget this step! (You can also start both scripts one after the other with only one script, this is up to you, but I did this separately so that if you do this on a terminal server you only have to start logging.bat once you restart the terminal server)

</details>

# Display results/display logs

To display the log files on another system (From this moment on I will call that system "adminsystem"), do the following:

<b><details><summary>Install</summary></b>
1. Install Python 5.5 or higher on the adminsystem as well
2. Start the "install/adminsys_install.bat" Skript on the adminsystem
3. Start the configurator (configurator.py) There, select the 2. Option. In this configurator you MUST now configure the database.
</details>

<b><details><summary>Usage</summary></b>
1. Start the "adminsessionstart.bat" file to start the virtual environment
2. Start the mySQL_Evaluation.py Skript
</details>

