import requests
import time
from etc.postgre.GQL import GQL
import re
from etc.helpers.helper import helper
from datetime import datetime

# initialise imports
gql_connector = GQL()


# Scryfall endpoints
URL_API_BULK = "https://api.scryfall.com/bulk-data"
urls =  'https://api.scryfall.com/cards/search?q=!%22Tarmogoyf'



def insertMtgToGQL(cards):
    i = 0
    bulk = {}
    for card in cards:
        if "object" in card.keys() and card["object"] == "error":
            i+=1
            continue
        if "image_uris" not in card.keys():
            i+=1
            continue
        else:
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
            power_cleaned = 0
            if 'power' in card.keys():
                if not card['power'].isdigit():
                    card['power_text'] = card['power']
                    card['power'] = None
                elif card['power'] == "∞":
                    power_cleaned = 'Infinity' 
                else:
                    power_cleaned = card['power']
            else:
              power_cleaned = None

            # Toughness clean-up
            toughness_cleaned = 0
            if 'toughness' in card.keys():
                if not card['toughness'].isdigit():
                    card['toughness_text'] = card['toughness']
                    card['toughness'] = None
                elif card['toughness'] == "∞":
                    toughness_cleaned = 'Infinity' 
                else:
                    toughness_cleaned = card['toughness']
            else:
              toughness_cleaned = None
              
            keywords_cleaned = ""
            if "keywords" in card.keys():
                if len(card["keywords"]) > 0:
                    for keyword in card["keywords"]:
                        keywords_cleaned = keywords_cleaned + "|" + keyword
            else:
                keywords_cleaned = None
    
    
            card_obj = helper.returnObject(  
                                       "mtg",                            # card_details.tcg
                                       card.get("id",""),                # card_details.api_id
                                       card.get("name",""),              # card_details.name
                                       card["image_uris"]["normal"],     # card_details.image
                                       card.get("set_name",""),          # card_details.set
                                       card.get("set",""),               # card_details.set_id
                                       card.get("collector_number",""),  # card_details.card_id
                                       card.get("rarity","").title(),    # card_details.rarity
                                       prices_cleaned,                   # card_details.price
                                       prices_foil_cleaned,              # card_details.price_foil
                                       prices_etched_cleaned,            # card_details.price_other
                                       card_type,                        # card_details.type
                                       card_subtype,                     # card_details.subtype
                                       card.get("oracle_text",None),     # card_details.game_text
                                       card.get("flavor_text",None),     # card_details.flavor_text
                                       card.get("cmc",None),             # card_details.cost
                                       card.get("mana_cost",None),       # card_details.cost_text
                                       power_cleaned,                    # card_details.attack
                                       toughness_cleaned,                # card_details.defence
                                       None,                             # card_details.kind
                                       None,                             # card_details.lotr_resistance ( NOT USED )
                                       keywords_cleaned,                 # card_details.keywords
                                       None,                             # card_details.lotr_culture ( NOT USED )
                                       None,                             # card_details.lotr_home_site ( NOT USED )
                                       card.get("power_text",None),      # card_details.mtg_attack_text
                                       card.get("toughness_text",None),  # card_details.mtg_toughness_text                   
                                    )
            bulk[i] = card_obj
            i+=1
            if i == 500:
                gql_connector.gqlInsertCards(list(bulk.values()))
                print(str(datetime.now()) + " Inserting bulk of 500")
                i=0
                bulk={}
    print(str(datetime.now()) + " Insertion complete")
                

def getScryfallApiBulkOracle(url):
    bulk_api_uri = ""
    api_response = requests.get(url).json()
    for data in api_response["data"]:
        if "type" in data:
            if data["type"] == "default_cards":
                bulk_api_uri = data["download_uri"]
    print(str(datetime.now()) + " Scryfall latest default_cards endpoing: " + bulk_api_uri)
    retryConnection(bulk_api_uri)
    api_bulk_response = requests.get(bulk_api_uri).json()
    tryConnetion(api_bulk_response)

# Fetch JSON from Scryfall's bulk endpoint
def getJSONfromApi(url):
    api_result = requests.get(url).json()
    return api_result

def tryConnetion(url):
    try:
        api_result = getJSONfromApi(url)
        return api_result
    except:
        print(str(datetime.now()) + " Failed to connect to Scryfall API")
        return None
    print(str(datetime.now()) + " Trying to get data from endpoint: " + str(url))

def retryConnection(url):
    retry_count = 10 
    for retry in range(retry_count):
        print(str(datetime.now()) + " Connecting to Scryfall API. Try: " + str(retry + 1))
        api_result = tryConnetion(url)
        if api_result == None:
            print(str(datetime.now()) + " Sleeping 15s...")
            time.sleep(15)
            continue
        else:
            cards = api_result
            print(str(datetime.now()) + " Success! Insertion in Progress")
            insertMtgToGQL(cards)
            break

# Where all magic happens
getScryfallApiBulkOracle(URL_API_BULK)

    