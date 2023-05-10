from faker import Faker
import psycopg2
import random
from book_api.models import BuyerSubscription
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

# Get the IDs of all Buyers
cur.execute("SELECT id FROM book_api_buyer")
buyer_ids = [row[0] for row in cur.fetchall()]

# Generate and insert 1,000,000 BuyerSubscription records
for i in range(1000000):
    buyer_id = random.choice(buyer_ids)
    start_date = fake.date_between(start_date="-1y", end_date="today")
    end_date = fake.date_between(start_date=start_date, end_date="+1y")

    # SQL query to insert a BuyerSubscription record
    query = "INSERT INTO book_api_buyersubscription (buyer_id, start_date, end_date) VALUES (%s, %s, %s)"
    values = (buyer_id, start_date, end_date)
    print(BuyerSubscription.obejcts.count())
    # Execute the SQL query
    try:
        cur.execute(query, values)
    except psycopg2.errors.UniqueViolation:
        # Skip the insertion if a unique constraint violation error is thrown
        conn.rollback()
        continue

    # Commit the changes to the database
    if i % 1000 == 0:
        conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
