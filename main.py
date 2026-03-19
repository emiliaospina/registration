## Logic: 
    # The main.py file serves as the entry point for the application, coordinating the setup of the database and launching the user interface.

# Import necessary modules and functions.
from create_database_and_table import create_database_and_table
from cli_menu import show_menu


# Function 1. Main function to run the application. It first ensures that the database and table exist by calling create_database_and_table(), and then launches the command-line menu for user interaction.
def main():
    try:
        # Ensure database and table exist before starting the app
        create_database_and_table()

        # Launch the command-line menu
        show_menu()

    except Exception as e:
        print(f"An error occurred while running the application: {e}")


if __name__ == "__main__":
    main()