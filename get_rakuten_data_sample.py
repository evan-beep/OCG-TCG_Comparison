import datetime
import json
import sqlite3
import numpy as np
import time
import requests


def get_rakuten():
    # API endpoint
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"

    def middle_points_average(data):
        sorted_data = np.sort(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return np.mean(sorted_data[(n//2 - 1):(n//2 + 1)])
        else:
            return sorted_data[n//2]

    rarity_dict = {
        'PSE': 'プリズマティックシークレット',
        'SR': 'スーパー',
        'SE': 'シークレット',
        'UL': 'アルティメット',
        'UR': 'ウルトラ',
        'HR': 'ホロ',
        'R': 'レア',
        'N': 'ノーマル',
        'NR': 'ノーマル',
        'QCSE': 'クォーターセンチュリー',
        'P-N': 'ノーマル',
        'CR': 'コレクターズレア'
    }
    # Connect to the SQLite database
    conn = sqlite3.connect('Card_Prices.db')
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS rakuten_prices (
                cardName TEXT,
                rarity TEXT,
                num TEXT,
                price INTEGER,
                set_name TEXT,
                DateTime TEXT,
                UNIQUE(cardName, rarity, num, DateTime)
            )
        ''')

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")

    # Use the formatted datetime in your SQL query
    query = f"""
        SELECT cardName, rarity, num
        FROM ocg_prices
        WHERE DateTime = '{current_datetime}'
    """

    cursor.execute(query)

    # Fetch all records that match the query
    records = cursor.fetchall()

    # Print each record
    for (cardName, r, num) in records:

        keyword = f'{num} {rarity_dict[r]}'
        print(keyword)
        # Parameters for the API call
        params = {
            # Replace [APPLICATION ID] with your actual application ID
            "applicationId": "1065074286901705246",
            "keyword": keyword,
            "sort": "+itemPrice"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            priceList = []
            for item in data['Items']:
                priceList.append(int(item['Item']['itemPrice']))
            price = 0

            try:
                price = min(priceList)
            except ValueError:
                price = 0

            cursor.execute('''
                        INSERT OR IGNORE INTO rakuten_prices (cardName, rarity, num, price, set_name, DateTime)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (cardName, r, num, price, num.split('-')[0], current_datetime))

        else:
            print("Failed to retrieve data:", response.status_code)
            print(response)

        time.sleep(0.65)
    print('All Done')
    # Close the connection to the database
    conn.commit()
    conn.close()
