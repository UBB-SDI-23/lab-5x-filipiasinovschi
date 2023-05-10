import psycopg2
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

cur.execute("SELECT id FROM book_api_book")
books = cur.fetchall()

cur.execute("SELECT id FROM book_api_buyer")
buyers = cur.fetchall()

for i in range(1000000):
    book_id = random.choice(books)[0]
    buyer_id = random.choice(buyers)[0]
    price = random.randint(1, 100)
    timestamp = datetime.now() - timedelta(days=random.randint(1, 365))
    query = "INSERT INTO book_api_purchase (book_id, buyer_id, price, timestamp) VALUES (%s, %s, %s, %s)"
    values = (book_id, buyer_id, price, timestamp)
    try:
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

cur.close()
conn.close()
