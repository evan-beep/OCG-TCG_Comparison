import requests
import datetime
import os
import csv

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

        # Collect data in records list
        for card in cards:
            for card_set in card.get('card_sets', []):
                if set_name in card_set['set_name']:  # Filter to only include the current set
                    record = {
                        'cardName': card['name'],
                        'rarity': card_set.get('set_rarity_code', 'N/A')[1:-1],
                        'set_edition': card_set.get('set_edition', 'N/A'),
                        'num': card_set['set_code'],  # Assuming 'num' is the card's ID
                        'tcgplayer_price': card_set.get('set_price', 'N/A'),
                        'cardmarket_price': card.get('card_prices', [])[0].get('cardmarket_price', 'N/A'),
                        'set': card_set['set_name'],
                        'set_abbv': card_set['set_code'].split('-')[0],
                        'DateTime': current_datetime
                    }
                    records.append(record)
        
        # Determine set abbreviation from the first appropriate record, if available
        set_abbv = records[0]['num'].split('-')[0] if records else 'NODATA'
        filename = f"data/{set_abbv}_{current_datetime}.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Write data to CSV
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['cardName', 'rarity', 'set_edition', 'num', 'tcgplayer_price', 'cardmarket_price', 'set','set_abbv', 'DateTime']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                writer.writerow(record)
                        
        print(f"Data saved to {filename}")
    else:
        print("Failed to retrieve data:", response.status_code, response.text)

# Example usage:
get_TCG_card_prices("Legend of Blue Eyes White Dragon")