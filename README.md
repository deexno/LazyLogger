![LazyEmploee](https://github.com/deexno/LazyLogger/blob/master/LazyEmploee.png "LazyEmploee")

# LazyLogger - About
LazyLogger is a program that allows administrators to record who forgets to lock the screen and who does not. LazyLogger is system independent and works on MacOS, Windows and Linux. LazyLogger also has the advantage that it requiers nothing more than a database, that means LazyLogger can run completely without a domain controller and can also be installed on computers that are not available in a domain. LazyLogger also has the advantage that it works on Terminal Servers.

# Requirements
All you need is a database with MySQL version 5.5 or higher
(If you do not have a db, you can create a database completely free online on sites such as https://www.freemysqlhosting.net/)

# Installation

## Windows, Linux and MacOS 
Start the Installer (installFiles/lazyLogger_win.exe - lazyLogger_linux.sh for Linux and MacOS) and put the LazyLogger.py into the autostart.
That's it lol.

<details><summary>For Windows-Terminal-Servers:</summary> 
If you want to set up LazyLogger on a terminal server do it like this:<br>
1. Install the LazyLogger on the Server 
2. Create a CPO under Policies/Windows Settings/Skripts which automatically starts the LazyLogger.py after a logon
</details>

# Display results/display logs
1. Start the "mySQL_Evaluation.py" Skript
2. Have fun

