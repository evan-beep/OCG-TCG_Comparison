'''
This file gets data from saved TCGPlayer txt files.
The txt files are manually saved from the website, no bots involved
'''

import re
import glob
from datetime import datetime

pattern = re.compile(
    r"(?P<rarity>.+?)·\s#(?P<code>\w+-\w+)\n\n"
    r"(?P<name>.+?)(?:\n\n|\n)" 
    r"(?:.*\n)*?" 
    r"Market Price:\$(?P<market_price>\d+\.\d+)" 
)

rarity_dict = {
    "Secret Rare": "SE",
    "Ultra Rare" : "UR",
    "Super Rare" : "SR",
    "Common / Short Print": "N",
    "Quarter Century Secret Rare": "QCSE"
}

def get_data_from_txt():
    csv_data = [["market", "rarity", "num", "price", "Currency", "Set", "Price Date"]]

    # folder is not kept
    folder_path = "tcgplayer_web\\*.txt"

    for filename in glob.glob(folder_path):
        with open(filename, 'r', encoding='utf-8') as file:
            text_content = file.read()

        matches = pattern.finditer(text_content)

        for match in matches:
            card_info = match.groupdict()
            # print(f"{rarity_dict[card_info['rarity']]} {card_info['code']} {card_info['market_price']}")
            csv_row = [
                "TCGPlayer",  # Market
                rarity_dict[card_info['rarity']],  # Rarity
                card_info['code'],  # Num (code)
                card_info['market_price'],  # Price,
                "USD", #Currency
                card_info['code'][:4], #Set ID,
                datetime.now().strftime('%Y-%m-%d')
            ]

            csv_data.append(csv_row)
    return csv_data

csv_file_path = 'DataTables\\tcgplayer.csv'

import csv
# Write data to CSV
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(get_data_from_txt())

