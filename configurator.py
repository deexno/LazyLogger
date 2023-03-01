from configparser import ConfigParser
from getpass import getpass

import inquirer
from inquirer.themes import GreenPassion

# initialize required variables
config = ConfigParser()
config.read("configFiles/database.ini")


# def for the general Config
def generalconf():
    config["general"]["locktime"] = input(
        "How long should it take to detect that "
        "the computer has not been locked?"
        f"\nCurrent saved value: {config['general']['locktime']} minutes"
        "\nThe input should be a number and is calculated in minutes: "
    )


# def for the db Config
def dbconf():
    config["database"]["host"] = input(
        "Enter the host name of the database\n"
        f"Current saved value: {config['database']['host']}: "
    )
    config["database"]["dbname"] = input(
        "Enter the name of the database\n"
        f"Current saved value: {config['database']['dbname']}: "
    )
    config["database"]["user"] = input(
        "Enter the username of the database\n"
        f"Current saved value: {config['database']['user']}: "
    )
    config["database"]["port"] = input(
        "Enter the port of the database\n"
        f"Current saved value: {config['database']['port']}: "
    )

    while True:
        password = getpass("Enter the password of the database: ")
        password2 = getpass("Confirm password: ")
        if password != password2:
            input(
                "The entered passwords are not equal - "
                "The password has not been saved!"
            )
        else:
            config["database"]["password"] = password
            break


# Start - Banner
print(f"{30 * '#'}\n" "lazyLogger - configuration\n" f"{30 * '#'}\n")

# Navigation

config_options = [
    "Everything",
    "The Database",
    "General settings",
    "X NOTHING X",
]

config_option_selection = inquirer.prompt(
    [
        inquirer.List(
            "selection",
            message="WHAT WOULD YOU LIKE TO CONFIGURE?",
            choices=config_options,
            default="",
        )
    ],
    theme=GreenPassion(),
)

selected_option = config_option_selection["selection"]

if selected_option == config_options[0]:
    generalconf()
    dbconf()
elif selected_option == config_options[1]:
    dbconf()
elif selected_option == config_options[2]:
    generalconf()
elif selected_option == config_options[3]:
    print("BYE.")

with open("configFiles/database.ini", "w") as configfile:
    config.write(configfile)
