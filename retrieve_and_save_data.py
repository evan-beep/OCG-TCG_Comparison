from get_all_sets import get_all_sets
from get_TCG_card_prices import get_TCG_card_prices
from get_OCG_card_prices import get_OCG_card_prices
import json

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def filter_sets(data):
    filtered_sets = {}
    for set_code, details in data.items():
        try:
            year = int(details['tcg_date'].split('-')[0])
            card_count = int(details.get('card_count', 0))  # Safe default if card_count is missing
            if year > 2020 and card_count > 100 and card_count < 150:
                filtered_sets[set_code] = details
        except ValueError:
            continue
    return filtered_sets

def main():
    # Assuming 'code_to_name.json' is in the same directory
    data = load_json_data('sets\\code_to_name.json')
    filtered_sets = filter_sets(data)
    print("Filtered sets released after 2020 with more than 30 cards:")
    for set_code, details in filtered_sets.items():
        print(f"Set Code: {set_code}, Set Names: {details['set_names']}, Release Date: {details['tcg_date']}, Card Count: {details['card_count']}")

if __name__ == "__main__":
    main()