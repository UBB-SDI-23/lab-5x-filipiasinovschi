from faker import Faker
import psycopg2
import random

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="postgres",
    password="postgres"
)

# Create a cursor object
cur = conn.cursor()

# Create a Faker instance
fake = Faker()

# Get the IDs of all Authors and Publishers
cur.execute("SELECT id FROM book_api_author")
author_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT id FROM book_api_publisher")
publisher_ids = [row[0] for row in cur.fetchall()]

# Generate and insert 1,000 Book records
for i in range(1000000):
    title = fake.sentence(nb_words=3)
    number_of_pages = random.randint(1, 1000)
    publish_date = fake.date_between(start_date="-10y", end_date="today")
    quantity = random.randint(1, 100)
    ibn = random.randint(10000, 99999)
    author_id = random.choice(author_ids)
    publisher_id = random.choice(publisher_ids)
    price = random.randint(10, 100)

    # SQL query to insert a Book record
    query = "INSERT INTO book_api_book (title, number_of_pages, publish_date, quantity, ibn, author_id, publisher_id, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
    values = (title, number_of_pages, publish_date, quantity, ibn, author_id, publisher_id, price)

    try:
        # Execute the SQL query
        cur.execute(query, values)

        # Get the ID of the inserted Book record
        book_id = cur.fetchone()[0]

        # Generate and insert 1-5 Buyer records for the Book
        for j in range(random.randint(1, 5)):
            name = fake.name()
            email = fake.email()

            # SQL query to insert a Buyer record
            query = "INSERT INTO book_api_buyer (name, email) VALUES (%s, %s) RETURNING id"
            values = (name, email)

            try:
                # Execute the SQL query
                cur.execute(query, values)

                # Get the ID of the inserted Buyer record
                buyer_id = cur.fetchone()[0]

                # SQL query to insert a record into the BookBuyers table
                query = "INSERT INTO book_api_book_buyers (book_id, buyer_id) VALUES (%s, %s)"
                values = (book_id, buyer_id)

                # Execute the SQL query
                cur.execute(query, values)

            except psycopg2.Error as e:
                print(f"Error inserting Buyer record: {e}")
                conn.rollback()

        # Commit the changes to the database
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error inserting Book record: {e}")
        conn.rollback()

# Close the cursor and connection
cur.close()
conn.close()
