from db_connection import get_db_connection
import bcrypt

# Function 1. If user updates password we need hashing function once again
def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

# Function 2. Update user information (email or password)
def update_user(username, field, new_value):
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

        # If user does not exist, print message and return
        if user is None:
            print(f"User '{username}' does not exist")
            return

        # Validate which field can be updated
        if field not in ["email", "password"]:
            print("Invalid field. You can only update 'email' or 'password'")
            return

        # Update password but first guarantees that user knows current password to avoid unauthorized changes
        if field == "password":
            # Ask for current password
            current_password = input("Enter your current password: ")

            # Get stored hashed password from DB
            get_password_query = "SELECT password FROM users WHERE username = %s"
            cursor.execute(get_password_query, (username,))
            result = cursor.fetchone()

            if result is None:
                print("User not found")
                return

            stored_hashed_password = result[0]

            # Verify stored password with password entered by user
            if not bcrypt.checkpw(current_password.encode("utf-8"), stored_hashed_password.encode("utf-8")):
                # If entered password does not match stored password, print message and return
                print("Incorrect current password. Cannot update password.")
                return

            # If correct, then hash new password
            new_value = hash_password(new_value)
                # Build the update query
                update_query = f"UPDATE users SET {field} = %s WHERE username = %s"
                cursor.execute(update_query, (new_value, username))
                conn.commit()

        # Checks number of affected rows to confirm update
        if cursor.rowcount > 0:
            print(f"{field.capitalize()} updated successfully for user '{username}'")
        else:
            print("No changes were made")

    except Exception as e:
        print(f"Error updating user: {e}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    username = input("Enter the username: ")
    field = input("What do you want to update? (email/password): ").strip().lower()
    new_value = input("Enter the new value: ")

    update_user(username, field, new_value)