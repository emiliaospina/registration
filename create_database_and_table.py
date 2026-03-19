from db_connection import get_db_connection, load_db_config


def create_database_and_table():
    # Read the database name from db.yaml
    config = load_db_config()
    db_name = config["database"]

    # 1) Connect to MySQL server only (without selecting a database yet)
    conn = get_db_connection(include_database=False)
    if conn is None:
        print("Could not connect to MySQL server")
        return

    cursor = conn.cursor()

    # 2) Create the database if it does not exist
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
    cursor.execute(create_database_query)
    print(f"Database '{db_name}' is ready")

    cursor.close()
    conn.close()

    # 3) Connect again, now including the database
    conn = get_db_connection(include_database=True)
    if conn is None:
        print("Could not connect to the database")
        return

    cursor = conn.cursor()

    # 4) Create the users table (guarantees unique and required values)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        city VARCHAR(255),
        company VARCHAR(255),
        job_title VARCHAR(255)
    )
    """

    cursor.execute(create_table_query)
    conn.commit()

    print("Table 'users' is ready")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_database_and_table()