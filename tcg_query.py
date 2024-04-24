import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('Card_Prices.db')
cursor = conn.cursor()

# Query to select records where tcgplayer_price is less than $5
cursor.execute("""
    SELECT cardName, rarity, set_edition, num, tcgplayer_price, cardmarket_price, set_name, set_abbv, DateTime
    FROM card_prices
    WHERE num = 'PHNI-EN019'
""")

# Fetch all records that match the query
records = cursor.fetchall()

# Print each record
for record in records:
    print(record)

# Close the connection to the database
conn.close()