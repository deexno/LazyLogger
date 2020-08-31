import sys, threading, time, pymysql.cursors, getpass
from pynput import keyboard
from configparser import ConfigParser

########################################################################################################################
# initialize required variables
########################################################################################################################
username = getpass.getuser()
lockcombination = {keyboard.Key.cmd}
lockcombination2 = {keyboard.Key.ctrl_l,keyboard.Key.alt_l, keyboard.Key.delete}
on_off_combination = {keyboard.Key.esc, keyboard.Key.page_down}
current = set()
treadrunning = False
locked = False
combination = ""
inactivity = False

# DB-conf-init
config = ConfigParser()
config.read('configFiles/database.ini')
dbname = config['database']['dbname']
host = config['database']['host']
user = config['database']['user']
password = config['database']['password']

# General-conf-init
locktime = config['general']['locktime']

########################################################################################################################
# Store database credentials in a variable/establish a connection to the DB
########################################################################################################################
connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO logins (username) VALUES (%s);"
        cursor.execute(sql, username)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    print("Successfull")
except:
    print("ERROR")

########################################################################################################################
# initialize the method run and inaktiv
########################################################################################################################
def inactive():
    global treadrunning
    global locked
    global connection
    global combination
    global inactivity
    sec = 0

    while True:
        time.sleep(1)
        print("inactive since: " + str(sec) + " Seconds")
        sec = sec + 1

        if inactivity == False:
            try:
                with connection.cursor() as cursor:
                    # Create a new record
                    print(username + " is active again!")
                    sql = "INSERT INTO inactivities (username, duration) VALUES (%s, %s);"
                    cursor.execute(sql, (username, int(sec)))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()

                print("Successfull")
            except:
                print("ERROR")
            break


def run():
    global treadrunning
    global locked
    global connection
    global combination
    global inactivity
    sec = 0

    while True:
        time.sleep(1)
        print(sec)
        sec = sec + 1
        if sec >= int(locktime) * 60:
            print("User... has forgotten to lock the screen")
            combination = ""
            locked = True  # User... has forgotten to lock the screen
            try:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO forgottenscreenlocks (username) VALUES (%s);"
                    cursor.execute(sql, username)

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()

                print("Successfull")
            except:
                print("ERROR")

        if treadrunning == False and locked == False:
            #Start a new thread and terminate the current one. 
            treadrunning = True
            t1 = threading.Thread(target=run)
            t1.start()
            break

        if locked == True:
            print("Locked")
            try:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO screenlocks (username, combination) VALUES (%s, %s);"
                    cursor.execute(sql, (username, combination))
                    inactivity = True
                    t2 = threading.Thread(target=inactive)
                    t2.start()

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()

                print("Successfull")
            except:
                print("ERROR")
            break


########################################################################################################################
# Start the method run as a thread/start to monitor the input of the Keyboard
########################################################################################################################

# Start the Logging
treadrunning = True
t1 = threading.Thread(target=run)
t1.start()


########################################################################################################################
# When a key on the keyboard is pressed, execute the following code
########################################################################################################################
def on_press(key):
    global treadrunning
    global locked
    global combination
    global inactivity

    #When this key combination is pressed, the program terminates
    if key in on_off_combination:
        current.add(key)
        if all(k in current for k in on_off_combination):
            locked = True
            print('LazyUserLogging was terminated')
            sys.exit()

    #Check whether one of the lock combinations was executed
    if key in lockcombination2:
        current.add(key)
        if all(k in current for k in lockcombination2):
            print('The screen has been locked')
            print(current)
            #Clear the array "current" so that not one of the keys is stored in it afterwards
            current.clear()
            combination = "Ctrl + Alt + Del"
            treadrunning = False
            locked = True

    if key in lockcombination:
        current.add(key)
        if all(k in current for k in lockcombination):
            print('The screen has been locked')
            print(current)
            #Clear the array "current" so that not one of the keys is stored in it afterwards
            current.clear()
            combination = "Win + L"
            treadrunning = False
            locked = True

    if locked == True and not key in lockcombination2 and not key in lockcombination:
        #The user has made an entry on the keyboard again! The timer is started again
        locked = False
        inactivity = False
        treadrunning = True
        t1 = threading.Thread(target=run)
        t1.start()
    else:
        #The user has pressed a key, the timer is reset to 0
        treadrunning = False

    #Indicate in the console that a key has been pressed
    print("#")

########################################################################################################################
# create a listener for the Keyboard
########################################################################################################################
def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        listener.join()
    except KeyError:
        print("listener = stopped")
