import requests
import sys
from GQL import GQL
import re
gql_connector = GQL()
urls = [
    'https://api.scryfall.com/cards/search?q=!"Snapcaster%20Mage"&unique=prints',
    'https://api.scryfall.com/cards/search?q=!"Abrupt%20Decay"&unique=prints',
    'https://api.scryfall.com/cards/search?q=!"Balance"&unique=prints',
    'https://api.scryfall.com/cards/search?q=!"Guttersnipe"&unique=prints',
    'https://api.scryfall.com/cards/search?q=!"Ponder"&unique=prints',
    'https://api.scryfall.com/cards/search?q=!"Brain%20Freeze"&unique=prints',
    'https://api.scryfall.com/cards/search?q=!"Serum%20Visions"&unique=prints',
    'https://api.scryfall.com/cards/search?q=!"Opposition"&unique=prints',
    'https://api.scryfall.com/cards/search?q=!"Thoughtseize"&unique=prints',
    'https://api.scryfall.com/cards/search?q=!"Counterspell"&unique=prints',
]



def cardSearch(url):
    mtg_cards = requests.get(url).json()
# option == 1 for printing card/cards/
# else insert to db
    def printInsert(option):
        if option == 1:
            print(card)

        else:
            card_types = card.get("type_line").split(" � ")
            card_types_cleaned = re.sub(r"[^a-zA-Z0-9.:;!?,\s+]","",card_types[0])
            card_types_list = card_types_cleaned.split("  ")
            if len(card_types_list) == 1:
                card_type = card_types_list[0]
                card_subtype = ""
            else:
                card_type = card_types_list[0]
                card_subtype = card_types_list[1]
            prices_cleaned = 0 if card["prices"]["usd"] is None else float(card["prices"]["usd"])
            prices_foil_cleaned = 0 if card["prices"]["usd_foil"] is None else float(card["prices"]["usd_foil"])
            prices_etched_cleaned = 0 if card["prices"]["usd_etched"] is None else float(card["prices"]["usd_etched"])

            # Power clean-up
            power_cleaned = ""
            if 'power' in card.keys():
              power_cleaned = int(card["power"])
            else:
              power_cleaned = None
              
            # Toughness clean-up
            toughness_cleaned = ""
            if 'toughness' in card.keys():
              toughness_cleaned = int(card["toughness"])
            else:
              toughness_cleaned = None
                
            
            gql_connector.gqlInsertGenericCard(
                                       "mtg",
                                       card.get("id",""),
                                       card.get("name",""),
                                       card["image_uris"]["normal"],
                                       card.get("set_name",""),
                                       card.get("set",""),
                                       card.get("collector_number",""),
                                       card.get("rarity","").title(),
                                       prices_cleaned,
                                       prices_foil_cleaned,
                                       prices_etched_cleaned,
                                       card_type,
                                       card_subtype,
                                       card.get("oracle_text",""),
                                       card.get("flavor_text",""),
                                       card.get("cmc",0),
                                       card.get("mana_cost",""),
                                       power_cleaned,
                                       toughness_cleaned

                                    )


    mtg_cards = requests.get(url).json()

    #loop through all cards
    for card in mtg_cards["data"]:
        printInsert(2)
        break

for url in urls:
    cardSearch(url)
    