import requests
import json

def get_all_sets():
    url = 'https://db.ygoprodeck.com/api/v7/cardsets.php'
    params = {}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        all_sets = response.json()
        code_to_name = {}
        name_to_code = {}
        
        for set_info in all_sets:
            # Update code_to_name dictionary
            if set_info['set_code'] not in code_to_name:
                code_to_name[set_info['set_code']] = {
                    'set_names': [set_info['set_name']],
                    'tcg_date': set_info.get('tcg_date', 'Unknown'),
                    'card_count': set_info.get('num_of_cards', 'Unknown')
                }
            else:
                code_to_name[set_info['set_code']]['set_names'].append(set_info['set_name'])
            
            # Update name_to_code dictionary
            if set_info['set_name'] not in name_to_code:
                name_to_code[set_info['set_name']] = {
                    'set_codes': [set_info['set_code']],
                    'tcg_date': set_info.get('tcg_date', 'Unknown'),
                    'card_count': set_info.get('num_of_cards', 'Unknown')
                }
            else:
                if set_info['set_code'] not in name_to_code[set_info['set_name']]['set_codes']:
                    name_to_code[set_info['set_name']]['set_codes'].append(set_info['set_code'])

        # Save the dictionaries to JSON files
        with open('sets\\code_to_name.json', 'w') as f:
            json.dump(code_to_name, f, indent=4)
        with open('sets\\name_to_code.json', 'w') as f:
            json.dump(name_to_code, f, indent=4)

        print("Data saved to code_to_name.json and name_to_code.json")
    else:
        print("Failed to retrieve data:", response.status_code, response.text)

if __name__ == '__main__':
    get_all_sets()