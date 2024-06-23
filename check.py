import sqlite3

from get_all_sets import get_all_sets

# Connect to the SQLite database
conn = sqlite3.connect('Card_Prices.db')
cursor = conn.cursor()
get_all_sets()
# List of tables
tables = ['ocg_prices', 'rakuten_prices', 'tcg_prices']

# Dictionary to store unique DateTime values
unique_datetime_values = {}

for table in tables:
    # Query to get unique DateTime values
    query = f"SELECT DISTINCT DateTime FROM {table}"
    cursor.execute(query)
    result = cursor.fetchall()
    unique_datetime_values[table] = [row[0] for row in result]

# Close the connection
conn.close()

# Display the results
for table, datetimes in unique_datetime_values.items():
    print(f"Unique DateTime values in {table}:")
    for dt in datetimes:
        print(dt)
    print()  # For better readability
