import requests
import datetime
import sqlite3
from bs4 import BeautifulSoup

def get_OCG_card_prices(set_name):
    url = f"https://yuyu-tei.jp/sell/ygo/s/{set_name}"
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup_ocg = BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Failed to retrieve webpage. Status code: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return

    # Open the database connection
    conn = sqlite3.connect('Card_Prices.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist, with a unique constraint
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ocg_prices (
            cardName TEXT,
            rarity TEXT,
            num TEXT,
            price INTEGER,
            set_name TEXT,
            DateTime TEXT,
            UNIQUE(cardName, rarity, num, DateTime)
        )
    ''')

    # Parse the HTML to collect data
    for cl in soup_ocg.find_all(id="card-list3"):
        rarity_name = cl.find(class_="py-2 d-inline-block px-2 me-2 text-white fw-bold")
        cards = cl.find_all(class_="col-md")
        for cd in cards:
            try:
                setNum = cd.find(class_="d-block border border-dark p-1 w-100 text-center my-2").text.strip()
                price_element = cd.find(class_="d-block text-end")
                if not price_element:
                    price_element = cd.find(class_="d-block text-end text-danger")
                price = int(price_element.text.split()[0].replace(",", "")) if price_element else 0
                cardName = cd.find('h4', class_='text-primary fw-bold')
                cardName = cardName.text if cardName else 'Unknown'
                
                # Insert data into the database
                cursor.execute('''
                    INSERT OR IGNORE INTO ocg_prices (cardName, rarity, num, price, set_name, DateTime)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (cardName, rarity_name.text if rarity_name else 'Unknown', setNum, price, set_name, current_datetime))

            except Exception as e:
                print(f"An error occurred while processing one of the cards: {e}")

    # Commit changes and close the database connection
    conn.commit()
    conn.close()

    print(f"OCG {set_name} Data saved to SQLite database")

if __name__ == "__main__":
    get_OCG_card_prices("AGOV")