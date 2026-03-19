from db_connection import get_db_connection
from rich.console import Console
from rich.table import Table

# Function 1. Reads users and extracts all fields except password, then displays them in a table format using the rich library. Alerts if no users are found.
def read_users():
    # Establish a database connection
    conn = get_db_connection()
    if conn is None:
        print("Database connection failed")
        return

    cursor = conn.cursor()

    # Run select query on all fields that are stored in table users
    query = """
    SELECT id, username, email, city, company, job_title
    FROM users
    """

    #Fetch all values, alert if empty
    try:
        cursor.execute(query)
        users = cursor.fetchall()

        if not users:
            print("No users found")
            return

        # Rich library to display users in a specific table format (prevents ugly tuples)
        console = Console()
        table = Table(title="Users")

        table.add_column("ID", justify="right")
        table.add_column("Username")
        table.add_column("Email")
        table.add_column("City")
        table.add_column("Company")
        table.add_column("Job Title")
        # (Avoid displaying password column)

        # Defines table template and fills it with values from the database, handling None values leaving blanks
        for user in users:
            table.add_row(
                str(user[0]),
                str(user[1]),
                str(user[2]),
                str(user[3]) if user[3] is not None else "",
                str(user[4]) if user[4] is not None else "",
                str(user[5]) if user[5] is not None else ""
            )

        console.print(table)

    except Exception as e:
        print(f"Error reading users: {e}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    read_users()