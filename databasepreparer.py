import pymysql.cursors
from configparser import ConfigParser

config = ConfigParser()
config.read('configFiles/database.ini')
dbname = config['database']['dbname']
host = config['database']['host']
user = config['database']['user']
password = config['database']['password']

connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "CREATE TABLE `screenlocks` (`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, `username` varchar(50) NOT NULL," \
              " `at_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        cursor.execute(sql)

        sql = "CREATE TABLE `forgottenscreenlocks` (`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, `username` varchar(50) NOT NULL," \
              " `at_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        cursor.execute(sql)

        sql = "CREATE TABLE `logins` (`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, `username` varchar(50) NOT NULL," \
              " `at_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        cursor.execute(sql)
        
        sql = "CREATE TABLE `inactivities` (`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, `username` varchar(50) NOT NULL, `duration` int NOT NULL)"
        cursor.execute(sql)

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    print("Successfull")
    input()
except:
    print("ERROR")