from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime, timedelta
import random
import time
import string

# Cassandra connection details
contact_points = ['127.0.0.1']  # Replace with your Cassandra contact points
port = 9042  # Replace with your Cassandra port
username = 'db_user'  # Replace with your Cassandra username
password = 'secret'  # Replace with your Cassandra password
keyspace = 'demo_keyspace'  # Replace with your Cassandra keyspace

# Authentication provider
auth_provider = PlainTextAuthProvider(username=username, password=password)
# Connect to the Cassandra cluster
cluster = Cluster(contact_points=contact_points, port=port, auth_provider=auth_provider)
session = cluster.connect(keyspace)

# Initialize variables
row_count = 0
start_time = time.time()

def get_future_datetime(minutes):
    current_datetime = datetime.now()
    future_datetime = current_datetime + timedelta(minutes=minutes)
    return future_datetime

def generate_random_string(number):
    return ''.join(random.choices(string.ascii_letters, k=number))

# Generate 1 million rows = 1000000 of data
for i in range(1000000):
    # Generate values for each column
    username = generate_random_string(10)
    email = generate_random_string(16)+'@gmail.com'
    status = random.randint(0,1)
    created_at = datetime.now()
    updated_at = get_future_datetime(random.randint(1,10))

    insert_query = """
        INSERT INTO users 
        (username, email, status, created_at, updated_at) 
        VALUES (%s, %s, %s, %s, %s)
    """

    # Insert the row into the Cassandra table
    session.execute(insert_query, (username, email, status, created_at, updated_at))

    # Increment row count
    row_count += 1
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print row count and elapsed time
    print(f"Rows inserted: {row_count} | Elapsed time: {elapsed_time:.2f} seconds")

# Close the connection
session.shutdown()
cluster.shutdown()
