import getpass
import locale
import os
import platform
import re
import socket
import sys
import time
import uuid
from configparser import ConfigParser
from datetime import datetime
from threading import Thread

import psutil
import pymysql.cursors
from pynput import keyboard
from pynput.mouse import Listener

working_directory = os.path.dirname(os.path.abspath(__file__))

currently_pressed_keys = set()
inactivitie_in_sec = 0
pause_counter = False
ignore_input = False
last_events = []
user_name = getpass.getuser()
absence_time_user_in_sec = 0
session_id = None
sql_status = ""

# DB-conf-init
config = ConfigParser()
config.read("configFiles/database.ini")
dbname = config["database"]["dbname"]
host = config["database"]["host"]
user = config["database"]["user"]
password = config["database"]["password"]

# General-conf-init
locktime = config["general"]["locktime"]

connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    db=dbname,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)


def log(status, message):
    global working_directory
    global last_events

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO logs (status, message) "
                f"VALUES ('{status}', '{message}');"
            )
            connection.commit()
    except Exception as e:
        last_events.append(
            "A problem occurred while trying to write "
            f"the last logs to the database! {e}"
        )

    with open(f"{working_directory}/lazylogger.log", "a") as log_file:
        log_file.write(f"{status} - {message} - {datetime.now()}")


def ignore_input_countdown():
    global ignore_input

    ignore_input = True
    time.sleep(15)
    ignore_input = False


def screen_locked(shortcut_used):
    global pause_counter
    global currently_pressed_keys
    global absence_time_user_in_sec
    global locktime

    last_events.append(f"THE SCREEN HAS BEEN LOCKED - {shortcut_used}")
    currently_pressed_keys.clear()

    pause_counter = True

    if shortcut_used == "By the Computer":
        # The user has not made any entries since the respective time, it is
        # assumed that he has not been at the PC since this time, which is why
        # this time is credited to him.
        absence_time_user_in_sec = float(locktime) * 60

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO forgotten_screen_locks "
                    "(user_id, host_system_id) "
                    f"VALUES ({lookup_user()}, {lookup_system()});"
                )
                connection.commit()
        except Exception as e:
            log("CRITICAL", e)
    else:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO manual_screen_locks "
                    "(user_id, host_system_id, screenlock_shortcut) "
                    f"VALUES ({lookup_user()}, {lookup_system()}, "
                    f"'{shortcut_used}');"
                )
                connection.commit()
        except Exception as e:
            log("CRITICAL", e)

    # If the user locks the screen with CTRL + ALT + DEL, he must click
    # "Lock" with the mouse afterwards. In order to prevent the user from
    # being logged further, his input is ignored for 15 seconds.
    ignore_input_countdown_thread = Thread(target=ignore_input_countdown)
    ignore_input_countdown_thread.start()


def user_activity_recognized():
    global inactivitie_in_sec
    global pause_counter
    global absence_time_user_in_sec

    if not ignore_input:
        inactivitie_in_sec = 0

        if pause_counter:
            last_events.append("THE USER CAME BACK. START COUNTING")

            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO user_absences "
                        "(user_id, host_system_id, absence_duration) "
                        f"VALUES ({lookup_user()}, {lookup_system()}, "
                        f"{absence_time_user_in_sec});"
                    )
                    connection.commit()
            except Exception as e:
                log("CRITICAL", e)

            absence_time_user_in_sec = 0
            pause_counter = False


def on_key_press(key):
    global currently_pressed_keys

    shortcut_1 = {keyboard.Key.cmd, keyboard.KeyCode(char="l")}
    shortcut_2 = {
        keyboard.Key.ctrl_l,
        keyboard.Key.alt_l,
        keyboard.Key.delete,
    }
    on_off_combination = {keyboard.Key.esc, keyboard.Key.page_down}

    currently_pressed_keys.add(key)

    if key in shortcut_1:
        if all(k in currently_pressed_keys for k in shortcut_1):
            screen_locked("WIN + L")
    elif key in shortcut_2:
        if all(k in currently_pressed_keys for k in shortcut_2):
            screen_locked("CTRL + ALT + DEL")
    else:
        user_activity_recognized()

    if key in on_off_combination:
        if all(k in currently_pressed_keys for k in on_off_combination):
            last_events.append("LAZYUSER LOGGER HAS BEEN TERMINATED!")
            sys.exit()


def on_key_release(key):
    global currently_pressed_keys

    try:
        currently_pressed_keys.remove(key)
    except Exception as e:
        last_events.append(e)


def on_mouse_move(x, y):
    user_activity_recognized()


def on_mouse_click(x, y, button, pressed):
    user_activity_recognized()


def on_mouse_scroll(x, y, dx, dy):
    user_activity_recognized()


def start_keyboard_listening():
    with keyboard.Listener(
        on_press=on_key_press, on_release=on_key_release
    ) as listener:
        listener.join()


def start_mouse_listening():
    with Listener(
        on_move=on_mouse_move,
        on_click=on_mouse_click,
        on_scroll=on_mouse_scroll,
    ) as listener:
        listener.join()


def lookup_user():
    global user_name
    global connection

    user_domain = "none"

    try:
        user_domain = os.environ["userdomain"]
    except KeyError:
        user_domain = "not recognised"
    except Exception as e:
        log("WARNING", e)

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM users "
            f"WHERE user_name='{user_name}' and user_domain='{user_domain}'"
        )

        result = cursor.fetchone()

        if result is None:
            cursor.execute(
                "INSERT INTO users (user_name, user_domain) "
                f"VALUES ('{user_name}', '{user_domain}')"
            )

            id = connection.insert_id()
            connection.commit()
        else:
            id = result["id"]

    return id


def lookup_system():
    global connection

    system_arcitecture = platform.machine()
    system_os = platform.system()
    system_os_release = platform.release()
    system_os_version = platform.version()
    system_hostname = socket.gethostname()
    system_ip = socket.gethostbyname(socket.gethostname())
    system_mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    system_processor = platform.processor()
    system_ram = (
        str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
    )
    system_time_zone = datetime.now().astimezone().tzname()
    system_language = locale.getdefaultlocale()[0]

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM host_systems "
            f"WHERE system_hostname='{system_hostname}'"
        )

        result = cursor.fetchone()

        if result is None:
            # Split into several lines for better readability
            cursor.execute(
                "INSERT INTO host_systems ("
                "system_hostname, "
                "system_ip, "
                "system_mac_address, "
                "system_arcitecture, "
                "system_os, "
                "system_os_release, "
                "system_os_version, "
                "system_processor, "
                "system_ram, "
                "system_time_zone, "
                "system_language) "
                f"VALUES ('{system_hostname}', "
                f"'{system_ip}', "
                f"'{system_mac_address}', "
                f"'{system_arcitecture}', "
                f"'{system_os}', "
                f"'{system_os_release}', "
                f"'{system_os_version}', "
                f"'{system_processor}', "
                f"'{system_ram}', "
                f"'{system_time_zone}', "
                f"'{system_language}')"
            )

            id = connection.insert_id()
            connection.commit()
        else:
            id = result["id"]
            cursor.execute(
                "UPDATE host_systems SET "
                f"system_hostname='{system_hostname}', "
                f"system_ip='{system_ip}', "
                f"system_mac_address='{system_mac_address}', "
                f"system_arcitecture='{system_arcitecture}', "
                f"system_os='{system_os}', "
                f"system_os_release='{system_os_release}', "
                f"system_os_version='{system_os_version}', "
                f"system_processor='{system_processor}', "
                f"system_ram='{system_ram}', "
                f"system_time_zone='{system_time_zone}', "
                f"system_language='{system_language}' "
                f"WHERE id = {id}"
            )

    return id


def counter():
    global pause_counter
    global inactivitie_in_sec
    global currently_pressed_keys
    global last_events
    global locktime
    global absence_time_user_in_sec
    global session_id
    global sql_status

    while True:
        time.sleep(1)

        print("\n" * 2, 20 * "-")
        last_events = last_events[-5:]

        print("Last 5 events: ")
        for event in last_events:
            print(event)

        print(f"\nCurrently pressed keys: {currently_pressed_keys}")
        print(f"SQL-DB Status: {sql_status}")

        if not pause_counter:
            inactivitie_in_sec += 1
            update_lazylogger_session(session_id, datetime.now(), 0)

            if inactivitie_in_sec >= float(locktime) * 60:
                screen_locked("By the Computer")
            else:
                print(f"Inactive since: {inactivitie_in_sec} sek")
        else:
            absence_time_user_in_sec += 1
            update_lazylogger_session(session_id, datetime.now(), 1)

            print("The counter is paused")
            print(f"The user is absence since: {absence_time_user_in_sec} sek")


def open_lazylogger_session():
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO active_logged_in_users "
                "(user_id, host_system_id, last_sign_of_life, screen_locked) "
                f"VALUES ({lookup_user()}, {lookup_system()}, "
                f"'{datetime.now()}', 0);"
            )
            session_id = connection.insert_id()
            connection.commit()
            return session_id
    except Exception as e:
        print("CRITICAL", e)


def close_lazylogger_session(session_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM active_logged_in_users WHERE id={session_id}"
            )
            connection.commit()
    except Exception as e:
        print("CRITICAL", e)


def update_lazylogger_session(session_id, last_sign_of_life, screen_locked):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE active_logged_in_users SET "
                f"last_sign_of_life='{last_sign_of_life}', "
                f"screen_locked='{screen_locked}' "
                f"WHERE id = {session_id}"
            )
            connection.commit()
    except Exception as e:
        print("CRITICAL", e)


def sql_session_check():
    global connection
    global last_events
    global sql_status

    while True:
        if not connection.open:
            try:
                log(
                    "CRITICAL",
                    "THE SQL SESSION IS CLOSED. "
                    "AN ATTEMPT WILL BE MADE TO REOPEN IT!",
                )
                connection = pymysql.connect(
                    host=host,
                    user=user,
                    password=password,
                    db=dbname,
                    charset="utf8mb4",
                    cursorclass=pymysql.cursors.DictCursor,
                )
                sql_status = "alive"
            except Exception as e:
                log("CRITICAL", e)
                sql_status = "death"
        else:
            sql_status = "alive"

        time.sleep(5)


sql_session_check_thread = Thread(target=sql_session_check)
sql_session_check_thread.start()

# WAIT FOR THE STATUS TO BE SET FOR THE SQL DB
print("PLEASE WAIT. LAZYLOGGER IS STARTING.")
time.sleep(3)
# Check initially whether all requirements are met for starting the programme.
if not sql_status == "alive":
    log("CRITICAL", "No connection to the database can be established!")
    log("CRITICAL", sql_status)
    os._exit(1)

# Initially check whether there is already an open session for the following
# user. If this is the case, cancel the programme start.
with connection.cursor() as cursor:
    cursor.execute(
        "SELECT id,last_sign_of_life FROM active_logged_in_users "
        f"WHERE user_id={lookup_user()}"
    )

    sessions = cursor.fetchall()
    active_sessions = []

    for session in sessions:
        session_id = session["id"]
        delta_time_difference = datetime.now() - session["last_sign_of_life"]
        delta_time_difference_in_sec = delta_time_difference.total_seconds()

        if delta_time_difference_in_sec >= 60:
            last_events.append(
                "An old session has been closed because "
                "it may no longer be active."
            )
            close_lazylogger_session(session_id)
        else:
            active_sessions.append(session_id)

    if len(active_sessions) == 0:
        last_events.append(
            "No active open connection was found for the "
            "respective user. A new session is opened."
        )
        session_id = open_lazylogger_session()
    else:
        log(
            "WARNING",
            "THERE IS ALREADY AN OPEN SESSION. " "LAZYLOGGER WILL BE STOPPED",
        )
        os._exit(1)

# NOTE THE LOGIN OF THE USER OR THAT HE HAS STARTED THE SCRIPT.
try:
    with connection.cursor() as cursor:
        # Create a new record
        cursor.execute(
            "INSERT INTO program_startups (user_id, host_system_id) "
            f"VALUES ({lookup_user()}, {lookup_system()});"
        )
        connection.commit()
except Exception as e:
    log("CRITICAL", e)


keyboard_listener_thread = Thread(target=start_keyboard_listening)
keyboard_listener_thread.start()

mouse_listener_thread = Thread(target=start_mouse_listening)
mouse_listener_thread.start()

counter_thread = Thread(target=counter)
counter_thread.start()
