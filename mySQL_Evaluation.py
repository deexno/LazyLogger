from configparser import ConfigParser
from datetime import datetime
import pymysql.cursors, os, time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

########################################################################################################################
## initialize required variables
########################################################################################################################
renewed_entry = True

# DB-conf-init
config = ConfigParser()
config.read('configFiles/database.ini')
dbname = config['database']['dbname']
host = config['database']['host']
user = config['database']['user']
password = config['database']['password']

########################################################################################################################
# Store database credentials in a variable/establish a connection to the DB
########################################################################################################################
connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def clear(): 
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    clear()
    person = ""
    timefrom = ""
    timetill = ""
    table = ""

    print(bcolors.WARNING + "#################################")
    time.sleep(0.1)
    print("# LazyUserMonitoring by. deexno #")
    time.sleep(0.1)
    print("#################################")
    time.sleep(0.1)
    print("#        mySQL-Evaluation       #")
    time.sleep(0.1)
    print("#################################\n\n")

    print(bcolors.BOLD + "What would you like to do?: ")
    print(bcolors.WARNING + "\n\nLogins:" + bcolors.ENDC + "\n0.0 List all Logins\n0.1 List all Logins in a certain period of time\n"
    "0.2 List all logins grouped by the name\n0.3 Count how often your selected person has logged in")
    print(bcolors.WARNING + "\n\nForgotten screenlocks:" + bcolors.ENDC + "\n1.0 List all forgotten screenlocks\n1.1 List all forgotten screenlocks in a certain period of time\n"
    "1.2 List all forgotten screenlocks grouped by the name\n1.3 Count how often your selected person has forgotten to lock the screen")
    print(bcolors.WARNING + "\n\nScreenlocks:" + bcolors.ENDC + "\n2.0 List all screenlocks\n2.1 List all screenlocks in a certain period of time\n"
    "2.2 List all screenlocks grouped by the name\n2.3 Count how often your selected person locked the screen")
    print(bcolors.WARNING + "\n\nInactivities:" + bcolors.ENDC + "\n3.0 List all inactivities\n3.1 List all inactivities in a certain period of time\n"
    "3.2 List all inactivities grouped by the name\n3.3 Count how often your selected person was inactive\n3.4 Count how often your selected person was inactive\n"
    "3.5 Count how long a selected person has been inactive")

    print(bcolors.FAIL + "\n\n\n99. Custom input\n\n\n")

    selection = input(bcolors.OKGREEN + "Your selection > " + bcolors.ENDC)

    if "99" in selection :
        table = ""
    elif "0." in selection :
        table = "logins"
    elif "1." in selection :
        table = "forgottenscreenlocks"
    elif "2." in selection :
        table = "screenlocks"
    elif "3." in selection:
        table = "inactivities"
    else:
        print("No such table available")
        input("Press enter to continue")

    if "99" in selection :
        sql = input(bcolors.WARNING +"LazyLogger@deexno:~# " + bcolors.ENDC)
    elif ".0" in selection :
        sql = "SELECT * FROM (%s)"
    elif ".1" in selection :
        timefrom = input("Starting with the date (Format = Year-Month-Day - ex. 2020-07-07): ")
        timetill = input("Ending with the date (Format = Year-Month-Day): ")
        sql = "SELECT * FROM (%s) WHERE username = (%s) AND at_date > (%s) AND at_date < (%s)"
    elif ".2" in selection :
        sql = "SELECT * FROM (%s) GROUP BY username"
    elif ".3" in selection:
        person = input("The name of the person: ")
        sql = "SELECT Count(username) AS Times FROM (%s) WHERE username = (%s)"
    elif ".4" in selection:
        person = input("The name of the person: ")
        sql = "SELECT SUM(duration) FROM (%s) WHERE username = (%s)"
    else:
        print("An unacceptable entry was made")
        input("Press enter to continue")

    try:
        with connection.cursor() as cursor:
            # Read a single record
            if person == "" and timefrom == "":
                cursor.execute(sql table)
            elif person != "" and timefrom == "":
                cursor.execute(sql, table, person)
            elif person == "" and timefrom != "":
                cursor.execute(sql, (table, timefrom, timetill))
            elif person != "" and timefrom != "":
                cursor.execute(sql, (table, person, timefrom, timetill))
            else:
                print("An error has occurred - The SQL code could not be executed successfully")

            connection.commit()
            result = cursor.fetchall()

            for i in result:
                print(bcolors.HEADER + str(i) + bcolors.ENDC)

            print("Successfull")
    except:
        print("ERROR")

    renewed_entry = input("Do you want to display another evaluation? (y/n): ")
    if renewed_entry.lower() != "y":
        break        