from get_all_sets import get_all_sets
from get_TCG_card_prices import get_TCG_card_prices
from get_OCG_card_prices import get_OCG_card_prices
from get_rakuten_data import get_rakuten
import json
import datetime
import time


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def filter_sets(data):
    filtered_sets = {}
    for set_code, details in data.items():
        try:
            year = int(details['tcg_date'].split('-')[0])
            # Safe default if card_count is missing
            card_count = int(details.get('card_count', 0))
            if year > 2022 and card_count == 101:
                filtered_sets[set_code] = details
        except ValueError:
            continue
    return filtered_sets


def main():

    # update sets every week
    # if datetime.datetime.now().weekday() == 3:
    #    get_all_sets()

    data = load_json_data('./sets/code_to_name.json')
    filtered_sets = filter_sets(data)

    for set_code, details in filtered_sets.items():
        get_OCG_card_prices(set_code)
        get_TCG_card_prices(details['set_names'][0])

    get_OCG_card_prices('INFO')  # patch, not perma fix
    get_OCG_card_prices('dp29')
    get_OCG_card_prices('ac04')
    get_OCG_card_prices('rota')
    get_OCG_card_prices('dbcb')
    get_OCG_card_prices('sd47')

    get_TCG_card_prices('Battles of Legend: Terminal Revenge')
    get_TCG_card_prices('The Infinite Forbidden')

    time.sleep(0.1)

    get_rakuten()


if __name__ == "__main__":
    main()
