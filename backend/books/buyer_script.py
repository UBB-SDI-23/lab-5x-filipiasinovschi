from faker import Faker
import psycopg2

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

# Generate and insert 1,000,000 Buyer records
for i in range(1000000):
    name = fake.name()
    email = fake.email()

    # SQL query to insert a Buyer record
    query = "INSERT INTO book_api_buyer (name, email) VALUES (%s, %s)"
    values = (name, email)

    # Execute the SQL query
    cur.execute(query, values)

    # Commit the changes to the database
    if i % 1000 == 0:
        conn.commit()

print("Buyers generated")