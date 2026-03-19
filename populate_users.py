## Logic:
    # 1. Import the Faker library and the create_user function from the create_user module.
    # 2. Define a function populate_users that takes an optional parameter n (default is 1000) which specifies the number of synthetic users to create.
    # 3. Inside the function, use a for loop to generate n synthetic users. For each user, generate a unique username, email, password, city, company, and job title using the Faker library.
    # 4. Call the create_user function with the generated user details to insert the user into the database.
    # 5. After the loop, print a message indicating that the synthetic users have been inserted successfully.

# Import packages
from faker import Faker
from create_user import create_user


fake = Faker()

# Function to populate the users table with synthetic data using Faker package
def populate_users(n=1000):
    for _ in range(n):
        username = fake.unique.user_name()
        email = fake.unique.email()
        password = fake.password(length=10)
        city = fake.city()
        company = fake.company()
        job_title = fake.job()

        create_user(username, email, password, city, company, job_title)

    print(f"{n} synthetic users inserted successfully")


if __name__ == "__main__":
    populate_users()