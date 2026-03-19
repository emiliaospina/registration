## Logic
    # 1. This file deletes a user from the users table based on the username
    # 2. It first connects to the database and checks whether the specified user exists
    # 3. If the user exists, it executes a DELETE query to remove the record
    # 4. It confirms whether the deletion was successful using the number of affected rows
    # 5. It handles the case where the username does not exist and closes the connection properly

#Import packages
from db_connection import get_db_connection

# Function 1. Deletes a user based on the username, first checks if the user exists and then deletes it, otherwise prints a message that the user does not exist.
def delete_user(username):
    conn = get_db_connection()
    if conn is None:
        print("Database connection failed")
        return

    cursor = conn.cursor()

    try:
        # First, check whether the user exists
        check_query = "SELECT id FROM users WHERE username = %s"
        cursor.execute(check_query, (username,))
        user = cursor.fetchone()

        # Return message if no match is found for the username entered by the user, otherwise proceed to delete the user
        if user is None:
            print(f"User '{username}' does not exist")
            return

        # Query to delete the user
        delete_query = "DELETE FROM users WHERE username = %s"
        cursor.execute(delete_query, (username,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"User '{username}' deleted successfully")
        else:
            print("No changes were made")

    # Error handling
    except Exception as e:
        print(f"Error deleting user: {e}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    username = input("Enter the username to delete: ")
    delete_user(username)