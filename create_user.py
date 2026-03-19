from db_connection import get_db_connection
import bcrypt

# Function 1. To hash the password using bcrypt (a secure hashing algorithm designed for passwords)
def hash_password(password):
    # Convert string to bytes to feed into bcrypt
    password_bytes = password.encode('utf-8')

    # Generate random salt (term salt refers to random data added to the password before hashing to make it more secure) and hash the password
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Convert back to string for storage in the database (guarantees database never sees original password)
    return hashed.decode('utf-8')

# Function 2. To create a new user in the database (takes user details, hashes the password, and stores everything securely in the users table)
def create_user(username, email, password, city, company, job_title):
    conn = get_db_connection()
    if conn is None:
        print("Database connection failed")
        return

    cursor = conn.cursor()

    # Hash the password before storing
    hashed_password = hash_password(password)

    # Parameterized query to prevent SQL injection (a security vulnerability where attackers can manipulate SQL queries by injecting malicious input) and guarantees format of data being inserted
    query = """
    INSERT INTO users (username, email, password, city, company, job_title)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (username, email, hashed_password, city, company, job_title)

    try:
        cursor.execute(query, values)
        conn.commit()
        print("User created successfully")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Define random test user details to create a new user in the database (this is just for testing purposes, in a real application we would get this data from user input)
    # Allows us also to test that the table doesnt allow for creation of duplicates for unique fields like username and email, and that the password is properly hashed in the database
    create_user(
        username="testuser",
        email="test@example.com",
        password="mypassword",
        city="Boston",
        company="MIT",
        job_title="Student"
    )