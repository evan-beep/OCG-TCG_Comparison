'''
This file gets data from saved Yuyu-Tei files.
The files are manually saved from the website, no bots involved
'''

from bs4 import BeautifulSoup
with open("yuyutei_web\\yuyutei.htm", "r", encoding="utf-8") as file:
    content_ocg = file.read()
   
csv_data = [["market", "rarity", "num", "price"]]

soup_ocg = BeautifulSoup(content_ocg, 'html.parser')
for cl in soup_ocg.find_all(id="card-list3"):
    rarity_name = cl.find(class_="py-2 d-inline-block px-2 me-2 text-white fw-bold")
    cards = cl.find_all(class_="col-md")
    for cd in cards:
        csv_row = []
        try:
            csv_row = [
                "Yuyu-Tei",
                rarity_name.text,
                cd.find(class_="d-block border border-dark p-1 w-100 text-center my-2").text,
                int(cd.find(class_="d-block text-end").text.split()[0].replace(",", ""))
            ]
        except:
            csv_row = [
                "Yuyu-Tei",
                rarity_name.text,
                cd.find(class_="d-block border border-dark p-1 w-100 text-center my-2").text,
                0
            ]
        csv_data.append(csv_row)
        
csv_file_path = 'Yuyu-tei.csv'

import csv
# Write data to CSV
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)

