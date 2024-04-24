import requests
import datetime
import sqlite3

def get_TCG_card_prices(set_name):
    url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
    params = {
        'cardset': set_name,
        'tcgplayer_data': 'true'
    }
    response = requests.get(url, params=params)
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if response.status_code == 200:
        cards = response.json()['data']
        records = []
        
        # Open the database connection
        conn = sqlite3.connect('Card_Prices.db')
        cursor = conn.cursor()
        
        # Create the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS card_prices (
                cardName TEXT,
                rarity TEXT,
                set_edition TEXT,
                num TEXT,
                tcgplayer_price REAL,
                cardmarket_price REAL,
                set_name TEXT,
                set_abbv TEXT,
                DateTime TEXT
            )
        ''')
        
        # Collect data and insert into the database
        for card in cards:
            for card_set in card.get('card_sets', []):
                if set_name in card_set['set_name']:  # Filter to only include the current set
                    print(card)
                    record = (
                        card['name'],
                        card_set.get('set_rarity_code', 'N/A'),
                        card_set.get('set_edition', 'N/A'),
                        card_set['set_code'],  # Assuming 'num' is the card's ID
                        card_set.get('set_price', 'N/A'),
                        card.get('card_prices', [])[0].get('cardmarket_price', 'N/A'),
                        card_set['set_name'],
                        card_set['set_code'].split('-')[0],
                        current_datetime
                    )
                    cursor.execute('''
                        INSERT INTO card_prices (cardName, rarity, set_edition, num, tcgplayer_price, cardmarket_price, set_name, set_abbv, DateTime)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', record)
        
        conn.commit()  # Commit changes to the database
        print("Data saved to SQLite database")
    else:
        print("Failed to retrieve data:", response.status_code, response.text)
    
    # Close the database connection
    conn.close()
get_TCG_card_prices("Phantom Nightmare")