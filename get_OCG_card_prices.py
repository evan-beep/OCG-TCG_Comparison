import requests
import datetime
import csv
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
            return  # Stop function if the webpage is not retrieved successfully
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return  # Stop function on request error

    csv_data = []

    # Assume card-list3 exists. If not, this part will skip without errors
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
                record = {
                    'cardName': cardName,
                    'rarity': rarity_name.text if rarity_name else 'Unknown',
                    'set_edition': '',
                    'num': setNum,
                    'price': price,
                    'set': set_name,
                    'DateTime': current_datetime
                }
                csv_data.append(record)
            except Exception as e:
                print(f"An error occurred while processing one of the cards: {e}")
                # Continue processing the rest of the cards even if one fails

    # Define the CSV file name
    filename = f"{set_name}_{current_datetime}.csv"
    fieldnames = ['cardName', 'rarity', 'set_edition', 'num', 'price', 'set', 'DateTime']

    # Write data to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in csv_data:
            writer.writerow(data)

    print(f"Data saved to {filename}")
