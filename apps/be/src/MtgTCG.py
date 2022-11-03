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

def checkField(field):
    if type(field) == "int":
        return type(field)
    if type(field) == "str":
        return type(field)
    if type(field) == "float":
        return type(field)
    if type(field) is None:
        return None


def cardSearch(urls):
    i = 1
    for url in urls:
        card = requests.get(url).json()
        if "object" in card.keys() and card["object"] == "error":
            print("Skipping " + str(i) + ": " + card.get("name",url))
            i+=1
            continue
        # else insert to db
        card_types = card.get("type_line").split(" � ")
        card_types_cleaned = re.sub(r"[^a-zA-Z0-9.:;!?,\s+]","",card_types[0])
        card_types_list = card_types_cleaned.split("  ")
        if len(card_types_list) == 1:
            card_type = card_types_list[0]
            card_subtype = None
        else:
            card_type = card_types_list[0]
            card_subtype = card_types_list[1]
        prices_cleaned = 0 if card["prices"]["usd"] is None else float(card["prices"]["usd"])
        prices_foil_cleaned = 0 if card["prices"]["usd_foil"] is None else float(card["prices"]["usd_foil"])
        prices_etched_cleaned = 0 if card["prices"]["usd_etched"] is None else float(card["prices"]["usd_etched"])
    
        # Power clean-up
        # 11111111 = *
        # 22222222 = -
        # 33333333 = +
        power_cleaned = ""
        if 'power' in card.keys():
          special_case = card["power"].replace("*","11111111").replace("+","33333333").replace("-","22222222")
          power_cleaned = int(special_case)
        else:
          power_cleaned = None
          
        # Toughness clean-up
        toughness_cleaned = ""
        if 'toughness' in card.keys():
          special_case = card["toughness"].replace("*","11111111").replace("+","33333333").replace("-","22222222")
          toughness_cleaned = int(special_case)
        else:
          toughness_cleaned = None
            
        time.sleep(0.1)
        print("Number " + str(i) + " : " + card.get("id",""))
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
                                   card.get("oracle_text",None),
                                   card.get("flavor_text",None),
                                   card.get("cmc",0),
                                   card.get("mana_cost",None),
                                   power_cleaned,
                                   toughness_cleaned,
                                   None
                                )
        i += 1

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
    