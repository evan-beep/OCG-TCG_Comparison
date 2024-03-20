'''
This file gets data from saved Yuyu-Tei files.
The files are manually saved from the website, no bots involved
'''

from bs4 import BeautifulSoup
from datetime import datetime
import glob

def get_data_from_htm():
    folder_path = "yuyutei_web\\*.htm"
    csv_data = [["market", "rarity", "num", "price", "Currency", "Set", "Price Date"]]

    for filename in glob.glob(folder_path):
        with open(filename, 'r', encoding='utf-8') as file:
            content_ocg = file.read() 
        soup_ocg = BeautifulSoup(content_ocg, 'html.parser')
        for cl in soup_ocg.find_all(id="card-list3"):
            rarity_name = cl.find(class_="py-2 d-inline-block px-2 me-2 text-white fw-bold")
            cards = cl.find_all(class_="col-md")
            for cd in cards:
                csv_row = []
                try:
                    setNum = cd.find(class_="d-block border border-dark p-1 w-100 text-center my-2").text
                    csv_row = [
                        "OCG",
                        rarity_name.text,
                        setNum,
                        int(cd.find(class_="d-block text-end").text.split()[0].replace(",", "")),
                        "JPY",
                        setNum[:4],
                        datetime.now().strftime('%Y-%m-%d')
                    ]
                except:
                    setNum = cd.find(class_="d-block border border-dark p-1 w-100 text-center my-2").text
                    csv_row = [
                        "OCG",
                        rarity_name.text,
                        setNum,
                        0,
                        "JPY",
                        setNum[:4],
                        datetime.now().strftime('%Y-%m-%d')
                    ]
                csv_data.append(csv_row)
    return csv_data

csv_file_path = 'DataTables\\yuyutei.csv'

import csv
# Write data to CSV
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(get_data_from_htm())

