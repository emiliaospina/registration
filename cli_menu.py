## Logic
    # 1. The CLI menu follows the CRUD operations defined in the respective functions (create_user, read_users, update_user, delete_user).
    # 2. To do so it creates a loop that continuously displays the menu until the user chooses to exit.
    # 3. Inside the loop, it prompts the user for their choice and calls the appropriate function based on that choice.
    # 4. Each function interacts with the database to perform the desired operation, and the results are displayed using the rich library for better formatting.

# Import necessary libraries and functions
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from create_user import create_user
from read_users import read_users
from update_user import update_user
from delete_user import delete_user
from db_connection import get_db_connection


console = Console()

# Function 1. To read/display one user based on the username provided by the user. It retrieves the user's details from the database and displays them in a formatted table. If the user is not found, it shows a warning message.
def read_one_user(username):
    conn = get_db_connection()
    if conn is None:
        console.print("[red]Database connection failed[/red]")
        return

    cursor = conn.cursor()

    query = """
    SELECT id, username, email, city, company, job_title
    FROM users
    WHERE username = %s
    """

    try:
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user is None:
            console.print(f"[yellow]User '{username}' not found[/yellow]")
            return

        table = Table(title=f"User: {username}")
        table.add_column("ID", justify="right")
        table.add_column("Username")
        table.add_column("Email")
        table.add_column("City")
        table.add_column("Company")
        table.add_column("Job Title")

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
        console.print(f"[red]Error reading user: {e}[/red]")

    finally:
        cursor.close()
        conn.close()


# Function 2. To show the menu and handle user input
def show_menu():
    while True:
        console.print(
            Panel.fit(
                "[bold cyan]User Registration System[/bold cyan]\n\n"
                "1. Create a new user\n"
                "2. Read/display one user\n"
                "3. Read/display all users\n"
                "4. Update an existing user\n"
                "5. Delete a user\n"
                "6. Exit",
                title="Main Menu"
            )
        )

        # Prompt the user for their choice and handle it accordingly, converting them to numbers for easier comparison and friendliness.
        choice = input("Enter your choice (1-6): ").strip()

        # Based on the user's choice, call the appropriate function to perform the desired operation
        if choice == "1":
            username = input("Enter username: ").strip()
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()
            city = input("Enter city: ").strip()
            company = input("Enter company: ").strip()
            job_title = input("Enter job title: ").strip()

            create_user(username, email, password, city, company, job_title)

        elif choice == "2":
            username = input("Enter username to display: ").strip()
            read_one_user(username)

        elif choice == "3":
            read_users()

        elif choice == "4":
            username = input("Enter username to update: ").strip()
            field = input("What do you want to update? (email/password): ").strip().lower()
            new_value = input("Enter the new value: ").strip()

            update_user(username, field, new_value)

        elif choice == "5":
            username = input("Enter username to delete: ").strip()
            delete_user(username)

        elif choice == "6":
            console.print("[bold green]Exiting application. Goodbye![/bold green]")
            break

        else:
            console.print("[red]Invalid choice. Please enter a number from 1 to 6.[/red]")


if __name__ == "__main__":
    show_menu()