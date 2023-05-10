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

# Generate and insert 1,000,000 Publisher records
for i in range(1000000):
    name = fake.company()
    address = fake.address()
    city = fake.city()
    country = fake.country()
    website = fake.url()
    age = fake.random_int(min=20, max=80)

    # SQL query to insert a Publisher record
    query = "INSERT INTO book_api_publisher (name, address, city, country, website, age) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (name, address, city, country, website, age)

    # Execute the SQL query
    cur.execute(query, values)

    # Commit the changes to the database
    if i % 1000 == 0:
        conn.commit()

# Close the cursor and connection
cur.close()
conn.close()