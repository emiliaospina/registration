## Logic
    # 1. This file is responsible for connecting Python to the MySQL server
    # 2. It loads the database credentials from the db.yaml file using PyYAML
    # 3. It defines a function to optionally connect either to the MySQL server only or to a specific database
    # 4. It returns the connection object if successful, or None if the connection fails
    # 5. A small test block at the bottom allows direct execution to verify that the connection works

import yaml
import mysql.connector
from mysql.connector import Error

# Function 1. To open YAML file with database configuration
def load_db_config():
    with open("db.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


# Function 2. To establish a connection to the MySQL database
def get_db_connection(include_database=True):       # Include database
    config = load_db_config()

    # Build the connection configuration based on the YAML file
    connection_config = {
        "host": config["host"],
        "user": config["user"],
        "password": config["password"],
        "port": config["port"]
    }

    if include_database:
        connection_config["database"] = config["database"]

    try:
        connection = mysql.connector.connect(**connection_config)
        if connection.is_connected():
            print("Connected to MySQL successfully")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


if __name__ == "__main__":
    conn = get_db_connection(include_database=False)
    if conn:
        print("Test connection worked")
        conn.close()
        print("Connection closed")