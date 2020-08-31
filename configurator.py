from configparser import ConfigParser
from getpass import getpass

########################################################################################################################
# initialize required variables
########################################################################################################################
config = ConfigParser()
config.read('configFiles/database.ini')


########################################################################################################################
# def for the general Config
########################################################################################################################
def generalconf():
    config['general']['locktime'] = input(
        "Enter how long it should take to detect that the computer has not been locked"
        "\nCurrent saved value: " + config['general']['locktime'] + " minutes"
        "\nThe input should be a number and is calculated in minutes: ")


########################################################################################################################
# def for the db Config
########################################################################################################################
def dbconf():
    config['database']['host'] = input("Enter the host name of the database\n"
                                       "Current saved value: " + config['database']['host'] + ": ")
    config['database']['dbname'] = input("Enter the name of the database\n"
                                         "Current saved value: " + config['database']['dbname'] + ": ")
    config['database']['user'] = input("Enter the username of the database\n"
                                       "Current saved value: " + config['database']['user'] + ": ")
    config['database']['port'] = input("Enter the port of the database\n"
                                        "Current saved value: " + config['database']['port'] + ": ")

    while True:
        password = getpass("Enter the password of the database: ")
        password2 = getpass("Confirm password: ")
        if password != password2:
            input("The entered passwords are not equal - The password has not been saved!")
        else:
            config['database']['password'] = password
            break


########################################################################################################################
# Start - Banner
########################################################################################################################
print('############################'
      '\n lazyLogger - configuration'
      '\n############################\n')

########################################################################################################################
# Navigation
########################################################################################################################
print("Config Options:\n1. Everything\n2. the Database\n3. general settings")
option = input("Select one of the options (1, 2 or 3): ")

if option == "1":
    generalconf()
    dbconf()
elif option == "2":
    dbconf()
elif option == "3":
    generalconf()
else:
    print("Your choice is not valid")

with open('configFiles/database.ini', 'w') as configfile:
    config.write(configfile)
