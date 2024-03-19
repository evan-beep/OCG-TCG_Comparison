'''
This file gets data from saved TCGPlayer txt files.
The txt files are manually saved from the website, no bots involved
'''

import re
import glob

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

csv_data = [["market", "rarity", "num", "price"]]

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
            card_info['market_price']  # Price
        ]

        csv_data.append(csv_row)

csv_file_path = 'TCGPlayer.csv'

import csv
# Write data to CSV
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)

