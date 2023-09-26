import mysql.connector
from datetime import datetime, timedelta
import string
import random

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="secret",
  database="demo_db"
)

mycursor = mydb.cursor()

def get_future_datetime(minutes):
    current_datetime = datetime.now()
    future_datetime = current_datetime + timedelta(minutes=minutes)
    return future_datetime

def generate_random_string(number):
    return ''.join(random.choices(string.ascii_letters, k=number))

sql = """
INSERT INTO users 
(username, email, status, created_at, updated_at) 
VALUES (%s, %s, %s, %s, %s)
"""
inserted_rows = 0
# Total 100 rows will be inserted
for i in range(10):
  value_list = []
  for j in range(10):
    inserted_rows += 1
    username = generate_random_string(10)
    email = generate_random_string(16)+'@gmail.com'
    status = random.randint(0,1)
    created_at = datetime.now()
    updated_at = get_future_datetime(random.randint(1,10))
    value_list.append((username, email, status, created_at, updated_at))
  
  mycursor.executemany(sql, value_list)

mydb.commit()

print(inserted_rows, "was inserted.")

mydb.close()