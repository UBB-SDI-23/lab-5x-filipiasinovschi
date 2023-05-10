from faker import Faker
import psycopg2
import random

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="mypostgres",
    password="postgres"
)

# Create a cursor object
cur = conn.cursor()

# Create a Faker instance
fake = Faker()

# Generate and insert 1,000,000 Author records
for i in range(100000):
    first_name = fake.first_name()
    last_name = fake.last_name()
    birth_date = fake.date_of_birth()
    email = fake.email()
    website = fake.url()

    # SQL query to insert an Author record
    query = "INSERT INTO book_api_author (first_name, last_name, birth_date, email, website) VALUES (%s, %s, %s, %s, %s)"
    values = (first_name, last_name, birth_date, email, website)

    # Execute the SQL query
    cur.execute(query, values)

    # Commit the changes to the database
    if i % 1000 == 0:
        conn.commit()

# Close the cursor and connection
cur.close()
conn.close()