import os
from configparser import ConfigParser

import pymysql.cursors

working_directory = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser()
config.read(f"{working_directory}/configFiles/database.ini")

dbname = config["database"]["dbname"]
host = config["database"]["host"]
user = config["database"]["user"]
password = config["database"]["password"]

connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    db=dbname,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)

try:
    with connection.cursor() as cursor:

        delete_all_tables = input(
            "Should all existing tables in the database "
            f"{dbname} be deleted?: (Y/N) "
        )

        if delete_all_tables == "Y":
            cursor.execute("SET foreign_key_checks = 0;")
            cursor.execute(
                "SELECT concat('DROP TABLE IF EXISTS `', table_name, '`;') as q "
                "FROM information_schema.tables "
                f"WHERE table_schema = '{dbname}';"
            )
            connection.commit()
            result = cursor.fetchall()

            for rows in result:
                cursor.execute(rows["q"])

            connection.commit()

        # Create a new record
        cursor.execute(
            "CREATE TABLE `users` ("
            "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "`user_name` varchar(100) NOT NULL, "
            "`user_domain` varchar(100))"
        )

        cursor.execute(
            "CREATE TABLE `host_systems` ("
            "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "`system_hostname` varchar(100) NOT NULL, "
            "`system_ip` varchar(100) NOT NULL, "
            "`system_mac_address` varchar(100), "
            "`system_arcitecture` varchar(100), "
            "`system_os` varchar(100), "
            "`system_os_release` varchar(100), "
            "`system_os_version` varchar(100), "
            "`system_processor` varchar(100), "
            "`system_ram` varchar(100), "
            "`system_time_zone` varchar(255), "
            "`system_language` varchar(64))"
        )

        cursor.execute(
            "CREATE TABLE `manual_screen_locks` ("
            "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "`user_id` int NOT NULL, "
            "`host_system_id` int NOT NULL, "
            "`screenlock_shortcut` varchar(25), "
            "`at_date_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "FOREIGN KEY (user_id) REFERENCES users(id), "
            "FOREIGN KEY (host_system_id) REFERENCES host_systems(id))"
        )

        cursor.execute(
            "CREATE TABLE `forgotten_screen_locks` ("
            "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "`user_id` int NOT NULL, "
            "`host_system_id` int NOT NULL, "
            "`at_date_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "FOREIGN KEY (user_id) REFERENCES users(id), "
            "FOREIGN KEY (host_system_id) REFERENCES host_systems(id))"
        )

        cursor.execute(
            "CREATE TABLE `program_startups` ("
            "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "`user_id` int NOT NULL, "
            "`host_system_id` int NOT NULL, "
            "`at_date_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "FOREIGN KEY (user_id) REFERENCES users(id), "
            "FOREIGN KEY (host_system_id) REFERENCES host_systems(id))"
        )

        cursor.execute(
            "CREATE TABLE `user_absences` ("
            "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "`user_id` int NOT NULL, "
            "`host_system_id` int NOT NULL, "
            "`absence_duration` int NOT NULL, "
            "`at_date_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "FOREIGN KEY (user_id) REFERENCES users(id), "
            "FOREIGN KEY (host_system_id) REFERENCES host_systems(id))"
        )

        cursor.execute(
            "CREATE TABLE `active_logged_in_users` ("
            "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "`user_id` int NOT NULL, "
            "`host_system_id` int NOT NULL, "
            "`screen_locked` BOOLEAN, "
            "`last_sign_of_life` timestamp, "
            "FOREIGN KEY (user_id) REFERENCES users(id), "
            "FOREIGN KEY (host_system_id) REFERENCES host_systems(id))"
        )

        cursor.execute(
            "CREATE TABLE `logs` ("
            "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "`status` varchar(64) NOT NULL, "
            "`message` varchar(4096) NOT NULL, "
            "`at_date_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )

        # Commit changes to the SQL Server
        connection.commit()

    input("Successfull. Press ENTER to exit the programme.")
except Exception as e:
    print(f"An error has occurred: {e}")
