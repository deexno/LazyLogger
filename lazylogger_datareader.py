from configparser import ConfigParser
from datetime import datetime

import inquirer
import pymysql.cursors
from inquirer.themes import GreenPassion

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


def list_items(table, filter="1=1"):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * from {table} WHERE {filter};")
            return cursor.fetchall()
    except Exception as e:
        print(e)
        return []


def list_all_items(table, start_date, end_date, user_id=None):

    filer_query = ""

    if user is not None:
        filer_query += f"user_id={user_id}"

    if start_date is not None:
        filer_query += f"at_date_time between '{start_date}' and '{end_date}'"

    items = list_items(
        table,
        f"at_date_time between '{start_date}' and '{end_date}' "
        f"and user_id={user_id}",
    )

    try:
        for item in items:
            print(item)
    except Exception as e:
        print(e)


def list_all_items_grouped_by_user(table, user, start_date, end_date):
    try:
        users = list_items("users")

        for user in users:
            user_name = user["user_name"]
            user_id = user["id"]
            items_count = list_items(table, f"WHERE user_id={user_id}")
            print(f"{user_name} - {items_count}")

    except Exception as e:
        print(e)


def user_picker():
    users_array = []
    users_dict = {}

    users = list_items("users")

    for user in users:
        full_user_name = f"{user['user_name']}@{user['user_domain']}"
        users_array.append(full_user_name)
        users_dict[full_user_name] = user["id"]

    user_selection = inquirer.prompt(
        [
            inquirer.List(
                "full_user_name",
                message="SELECT A USER",
                choices=users_array,
                default="",
            )
        ],
        theme=GreenPassion(),
    )

    return users_dict[user_selection["full_user_name"]]


def date_validation(answers, current):
    if not current.isnumeric() or len(current) > 4:
        raise inquirer.errors.ValidationError(
            "", reason="Your input does not meet the requirements!"
        )

    return True


def date_picker():
    date = [
        inquirer.Text("day", message="DAY", validate=date_validation),
        inquirer.Text("month", message="MONTH", validate=date_validation),
        inquirer.Text("year", message="YEAR", validate=date_validation),
    ]

    return f"{date['year']}/{date['month']}/{date['day']}"


tables = [
    "host_systems",
    "users",
    "manual_screen_locks",
    "forgotten_screen_locks",
    "program_startups",
    "user_absences",
    "active_logged_in_users",
    "logs",
]

menu_items = [
    "All rows in the table",
    "All rows in the table from a specific user",
    "All rows in the table grouped by the user",
]

display_options = inquirer.prompt(
    [
        inquirer.List(
            "table",
            message="WHICH TABLE WOULD YOU LIKE TO READ FROM?",
            choices=tables,
            default="",
        ),
        inquirer.List(
            "menu_option",
            message="WHAT EXACTLY DO YOU WANT TO DISPLAY?",
            choices=menu_items,
            default="",
        ),
        inquirer.List(
            "filer_for_timerange",
            message="DO YOU WANT TO FILTER ON A TIME PERIOD?",
            choices=["YES", "NO"],
            default="NO",
        ),
    ],
    theme=GreenPassion(),
)

selected_table = display_options["table"]
selected_menu_option = display_options["menu_option"]

filer_for_timerange = display_options["filer_for_timerange"]
start_date = None
end_date = None

if filer_for_timerange == "YES":
    print("ENTER THE START OF THE TIME RANGE: ")
    start_date = date_picker()

    print("ENTER THE END OF THE TIME RANGE: ")
    end_date = date_picker()

if selected_menu_option == menu_items[0]:
    list_all_items(selected_table, start_date, end_date)
elif selected_menu_option == menu_items[1]:
    list_all_items(selected_table, start_date, end_date, user_picker())
elif selected_menu_option == menu_items[2]:
    list_all_items_grouped_by_user(
        selected_table, user_picker(), start_date, end_date
    )
