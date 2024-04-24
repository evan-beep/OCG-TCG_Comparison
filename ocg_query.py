import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('Card_Prices.db')
cursor = conn.cursor()

# Query to select records where tcgplayer_price is less than $5
cursor.execute("""
    SELECT cardName, rarity, num, price, DateTime
    FROM ocg_prices
    WHERE rarity = 'QCSE'
""")

# Fetch all records that match the query
records = cursor.fetchall()

# Print each record
for record in records:
    print(record)

# Close the connection to the database
conn.close()