import requests
import time
from GQL import GQL
import re
import scrython

# initialise imports
gql_connector = GQL()

#urls = [
#    'https://api.scryfall.com/cards/search?q=!"Snapcaster%20Mage"&unique=prints',
#    'https://api.scryfall.com/cards/search?q=!"Abrupt%20Decay"&unique=prints',
#]



def cardSearch(urls):
    for url in urls:
        card = requests.get(url).json()
        if "object" in card.keys() and card["object"] == "error":
            continue
        # option == 1 for printing card/cards/
        # else insert to db
        time.sleep(0.5)
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
            
        time.sleep(0.5)
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
    

def getAllMagicLinks():
    urls = []
    URL = "https://api.scryfall.com/cards/" #https://api.scryfall.com/cards/grn/81
    all_sets = scrython.sets.Sets()
    for i, set_object in enumerate(all_sets.data()):
        set_code = all_sets.data(i,"code")
        set_card_count = all_sets.data(i,"card_count")
        for x in range(set_card_count):
            urls.append(URL + set_code + "/" + str(x))
    return urls
        
# Where all magic happens
cardSearch(getAllMagicLinks())
    