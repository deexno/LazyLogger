![LazyEmploee](https://github.com/deexno/LazyLogger/blob/master/LazyEmploee.png "LazyEmploee")

# LazyLogger - About
LazyLogger is a program that allows administrators to record who forgets to lock the screen and who does not. LazyLogger is system independent and works on MacOS, Windows and Linux. LazyLogger also has the advantage that it requiers nothing more than a database, that means LazyLogger can run completely without a domain controller and can also be installed on computers that are not available in a domain. LazyLogger also has the advantage that it works on Terminal Servers.

# Requirements
All you need is a database with MySQL version 5.5 or higher
(If you do not have a db, you can create a database completely free online on sites such as https://www.freemysqlhosting.net/)

# Installation
1. Download this repository and navigate to the downloaded directory.
2. Install Python 3.10 or a higher version.
3. If you don't already have it, install Pip3.
4. Use pip to install all necessary libraries by typing the following command:
```
pip3 install pymysql pynput configparser inquirer stubs psutil types-PyMySQL pyinstaller
```
5. Run the "configurator.py" and "database_preparer.py" files.
6. Create an executable file that you can install later on the target system. Keep in mind that the target system must have the same operating system as the one on which you're creating the executable file. For instance, if you want to create an executable file for Linux, run the following command on Linux. If you want to create an executable file for MacOS, run it on MacOS, and so on:
```
pyinstaller --onefile lazyLogger.pyw
```
You can now copy the executable file to the target system and add it to the autostart.

# Display results/display logs
You have the flexibility to use any visualization tool you prefer, be it Grafana, Power BI, or any other software to display your data.
