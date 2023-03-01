echo "Don't forget to install Python 3.5.0!!!"

pip3 install pymysql pynput configparser inquirer stubs psutil types-PyMySQL

python3 ../configurator.py

clear

echo "Now start the databasepreparer.py to set up the database (if you have not already done so). This will not be started automatically for security reasons!"
read "The installation was successful Press Enter to finish the installation!"
