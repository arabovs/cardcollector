import requests
import time
from etc.postgre.GQL import GQL
import re
import scrython
from etc.helpers.helper import helper
import json
from datetime import datetime

# initialise imports
gql_connector = GQL()
URL_API_BULK = "https://api.scryfall.com/bulk-data"


#urls = [
#    'https://api.scryfall.com/cards/search?q=!"Snapcaster%20Mage"&unique=prints',
#    'https://api.scryfall.com/cards/search?q=!"Abrupt%20Decay"&unique=prints',
#]
# https://api.scryfall.com/bulk-data
# https://api.scryfall.com/bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e
def checkField(field):
    if type(field) == "int":
        return type(field)
    if type(field) == "str":
        return type(field)
    if type(field) == "float":
        return type(field)
    if type(field) is None:
        return None


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
            # 11111111 = *
            # 22222222 = -
            # 33333333 = +
            power_cleaned = ""
            if 'power' in card.keys():
                if card['power'] == "∞":
                    power_cleaned = 'Infinity'
                else:
                    special_case = card["power"].replace("*","11111111").replace("+","33333333").replace("-","22222222").replace("?","44444444")
                    try:
                        power_cleaned = float(special_case)
                    except:
                        continue
            else:
              power_cleaned = None

            # Toughness clean-up
            toughness_cleaned = ""
            if 'toughness' in card.keys():
                if card['toughness'] == "∞":
                    toughness_cleaned = 'Infinity' 
                else:
                    special_case = card["toughness"].replace("*","11111111").replace("+","33333333").replace("-","22222222").replace("?","44444444")
                    try:
                        toughness_cleaned = float(special_case)
                    except:
                        continue
            else:
              toughness_cleaned = None
            card_obj = helper.returnObject(  "mtg",
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
                                       card.get("cmc",None),
                                       card.get("mana_cost",None),
                                       power_cleaned,
                                       toughness_cleaned,
                                       None)
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
    api_response = requests.get(URL_API_BULK).json()
    for data in api_response["data"]:
        if "type" in data:
            if data["type"] == "oracle_cards":
                bulk_api_uri = data["download_uri"]
    print(bulk_api_uri)
    retryConnection(bulk_api_uri)
    api_bulk_response = requests.get(bulk_api_uri).json()
    tryConnetion(api_bulk_response)

# Fetch JSON from Blizzard's endpoint
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

    