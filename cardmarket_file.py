from bs4 import BeautifulSoup

with open('page.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
    
soup = BeautifulSoup(html_content, 'lxml')
table_body = soup.find(class_='table_body')

if table_body:
    rows = table_body.find_all('div', recursive=False)

    for row in rows:
        card_details = row.find(class_="col-10 col-md-8 px-2 flex-column align-items-start justify-content-center")
        rarity_span = row.find('span', class_="icon rarity-icon")  # Look for the span with the specified class
        price = row.find(class_="col-price pe-sm-2")

        if card_details and rarity_span and price:
            card_name = card_details.text.strip()
            rarity = rarity_span.get('data-original-title')  # Extract the data-original-title attribute
            card_price = price.text.strip()

            print(f"Card Name: {card_name}, Rarity: {rarity}, Price: {card_price}")
else:
    print("The table_body class was not found in the provided HTML content.")
