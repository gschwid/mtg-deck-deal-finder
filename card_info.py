import requests
from bs4 import BeautifulSoup
import re

def find_link(deck):
    found_link = None
    url = f'https://mtgjson.com/api/v5/decks/'
    response = requests.get(url)
    data = response.content
    
    # Create HTML parser
    soup = BeautifulSoup(data, "html.parser")
    files = soup.find_all("td",class_ = 'link')

    # Find the link with the deck name that only contains one period
    for deck_link in files:
        if (deck in deck_link.text) and (contains_one_period(deck_link.text)):
            found_link = deck_link.text
    
    return found_link     

def fix_deck_name(deck):
    random_upper_s = deck.replace("'s", "S")
    deck = re.sub(r'[^a-zA-Z]', '', deck)
    random_upper_s = re.sub(r'[^a-zA-Z]', '', random_upper_s)

    # Some of the files use that stupid random upper s
    return (deck, random_upper_s)

def get_commander(deck):

    deck, deck_with_s = fix_deck_name(deck)
    deck_link = find_link(deck)

    # Checking if deck with upper S is needed to be used
    if deck_link == None:
        deck_link = find_link(deck_with_s)

    url = f'https://mtgjson.com/api/v5/decks/{deck_link}'
    response = requests.get(url)
    data = response.json()

    # Get commander name and scryfall id
    commander = data['data']['commander'][0]
    name = commander['name']
    scryfall_id = commander['identifiers']['scryfallId']

    # Get price and picture
    scryfall_url = f'https://api.scryfall.com/cards/{scryfall_id}'
    scryfall_response = requests.get(scryfall_url)
    scryfall_data = scryfall_response.json()
    prices = scryfall_data['prices']
    picture_url = scryfall_data['image_uris']['normal']

    # Picking price depending on if its a foil card 
    if prices['usd'] is not None:
        price = float(prices['usd'])
    else:
        price = float(prices['usd_foil'])

    print(f"{(name,picture_url,price)}")
    return (name,picture_url,price)

def get_expensive_cards(deck):

    deck, deck_with_s = fix_deck_name(deck)
    deck_link = find_link(deck)

    # Checking if deck with upper S is needed to be used
    if deck_link == None:
        deck_link = find_link(deck_with_s)

    url = f'https://mtgjson.com/api/v5/decks/{deck_link}'
    response = requests.get(url)
    data = response.json()

    deck_list = data['data']['mainBoard']
    total_cost_of_cards = 0
    most_expensive_card = ('','',0)
    second_expensive_card = ('','',0)
    third_expensive_card = ('','',0)
    fourth_expensive_card = ('','',0)

    for card in deck_list:

        # Extract card name and scryfall id
        name = card['name']
        scryfall_id = card['identifiers']['scryfallId']
        
        # Lookup scryfall id for price and picture
        scryfall_url = f'https://api.scryfall.com/cards/{scryfall_id}'
        scryfall_response = requests.get(scryfall_url)
        scryfall_data = scryfall_response.json()
        prices = scryfall_data['prices']
        picture_url = scryfall_data['image_uris']['normal']

        # Picking price depending on if its a foil card 
        if prices['usd'] is not None:
            price = float(prices['usd'])
        else:
            price = float(prices['usd_foil'])

        # Updating the expensive cards
        if most_expensive_card[2] < price:
            fourth_expensive_card = third_expensive_card
            third_expensive_card = second_expensive_card
            second_expensive_card = most_expensive_card
            most_expensive_card = (name, picture_url, price)
        
        elif second_expensive_card[2] < price:
            fourth_expensive_card = third_expensive_card
            third_expensive_card = second_expensive_card
            second_expensive_card = (name, picture_url, price)
        
        elif third_expensive_card[2] < price:
            fourth_expensive_card = third_expensive_card
            third_expensive_card = (name, picture_url,price)
        
        elif fourth_expensive_card[2] < price:
            fourth_expensive_card = (name, picture_url,price)

        total_cost_of_cards += price # Finding total amount of value in cards

    print(f"{most_expensive_card} {second_expensive_card} {third_expensive_card} {fourth_expensive_card}")
    return [most_expensive_card, second_expensive_card, third_expensive_card, fourth_expensive_card, total_cost_of_cards]

def contains_one_period(s):
    return s.count('.') == 1


