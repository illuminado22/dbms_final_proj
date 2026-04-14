import mariadb

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",       # change to your MariaDB username
    "password": "",       # change to your MariaDB password
    "database": "repository"
}

def get_conn():
    return mariadb.connect(**DB_CONFIG)
