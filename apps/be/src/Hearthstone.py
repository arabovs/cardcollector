import requests
import json
import time
from datetime import datetime

from etc.postgre.GQL import GQL
from etc.hearthstone.metadata import metadata
from etc.helpers.helper import helper

AUTH_URL = 'https://oauth.battle.net/token'
GAME_CODE = "hs"

## can make this better by using next_page
url_pages = [
"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&pageSize=500",
"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&page=2&pageSize=500",
"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&page=3&pageSize=500",
"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&page=4&pageSize=500",
"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&page=5&pageSize=500",
"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&page=6&pageSize=500",
"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&page=7&pageSize=500",
"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&page=8&pageSize=500",
"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&page=9&pageSize=500",
]

gql_connector = GQL() # initialise postgre connector


# Get token from Blizzard's AUTH_URL
def getAuthToken():
    params = {
        'client_secret': 'bPF7i3iMBs6GrsSUaaHTRnFhn25ZCHvI',
        'grant_type': 'client_credentials',
        'client_id': '7af929a351344362909d803901df5897',
    }

    print(str(datetime.now()) + " Getting Access Token...")
    response = requests.post(AUTH_URL, data=params)
    access_token = json.loads(response.text.replace("'", "\""))["access_token"]
    print(str(datetime.now()) + " Access Token: " + access_token)
    return access_token

AUTH_TOKEN = getAuthToken()

# Fetch JSON from Blizzard's endpoint
def getJSONfromApi(access_token, endpoint):
    api_result = requests.get(endpoint + "\&access_token=" + access_token).json()
    return api_result

# Initialise cards JSON 
cards = None
api_result = None

def tryConnetion(url):
    try:
        api_result = getJSONfromApi(AUTH_TOKEN,url)
        return api_result
    except:
        print(str(datetime.now()) + " Failed to connect to Blizzard API")
        return None
    

# takes a card objects and cleans various fields as per db model
def cleanupCard(card):
    
    # clean up classId classes
    if "classId" in card:
        for type in metadata["classes"]:
            for key, value in type.items():
                if key == "id" and value == card["classId"]:
                    card["classId"] = type["name"]
                    break    
    
    # clean up cardTypeId
    if "cardTypeId" in card:
        for type in metadata["types"]:
            for key, value in type.items():
                if key == "id" and value == card["cardTypeId"]:
                    card["cardTypeId"] = type["name"]
                    break
    else:
        card["cardTypeId"] = None


    # clean up minionTypes 
    if "minionTypeId" in card:
        for type in metadata["minionTypes"]:
            for key, value in type.items():
                if key == "id" and value == card["minionTypeId"]:
                    card["minionTypeId"] = type["name"]
                    break
    else:
        if card["cardTypeId"] == "Minion":
            card["minionTypeId"] = "Generic"
        else:
            card["minionTypeId"] = None
    
    # clean up rarityId
    if "rarityId" in card:
        for rarity in metadata["rarities"]:
            for key, value in rarity.items():
                if key == "id" and value == card["rarityId"]:
                    card["rarityId"] = rarity["name"]
                    break
    else:
        card["rarityId"] = None
        
    # clean up cardSetId
    if "cardSetId" in card:
        for setId in metadata["sets"]:
            for key, value in setId.items():
                if key == "id" and value == card["cardSetId"]:
                    card["cardSetIdOld"] = card["cardSetId"]
                    card["cardSetId"] = setId["name"]
                    break
    else:
        card["cardSetId"] = None
           
    # clean up attack and health
    if "attack" in card.keys():
        card["attack"] = float(card["attack"])
    else:
        card["attack"] = None
    
    if "health" in card.keys():
        card["health"] = float(card["health"])
    else:
        card["health"] = None
             
    # clean up manaCost
    if "manaCost" in card.keys():
        card["manaCost"] = float(card["manaCost"])
    else:
        card["manaCost"] = None
    
    return card

# insert into db
def insertIntoDatabase(cards):
    print(str(datetime.now()) + " Inserting cards")
    #for card in cards: # for metadata
    i = 0
    bulk = {}
    for card in cards["cards"]: # for all cards
        card = cleanupCard(card) # clean up required for all cards as part standartization
        bulk[i] = helper.returnObject(
                GAME_CODE,                             # card_details.tcg
                str(card.get("slug","")),              # card_details.api_id
                card.get("name",""),                   # card_details.name
                card.get("image",""),                  # card_details.image
                str(card.get("cardSetId",None)),       # card_details.set
                str(card.get("cardSetIdOld","")),      # card_details.set_id
                str(card.get("id",None)),              # card_details.card_id
                str(card.get("rarityId",None)),        # card_details.rarity
                None,                                  # card_details.price
                None,                                  # card_details.price_foil
                None,                                  # card_details.price_other
                str(card.get("cardTypeId",None)),      # card_details.type
                card.get("minionTypeId",None),         # card_details.subtype
                card.get("text",None),                 # card_details.game_text
                card.get("flavorText",None),           # card_details.flavor_text
                card["manaCost"],                      # card_details.cost
                None,                                  # card_details.cost_text
                card["attack"],                        # card_details.attack
                card["health"],                        # card_details.defence
                card.get("classId",None),              # card_details.kind
        )
        i+=1
    gql_connector.gqlInsertCards(list(bulk.values()))
    print(str(datetime.now()) + " Insertion Complete")

# loops through pages of 500 cards
for url in url_pages:
    print(str(datetime.now()) + " Trying to get data from endpoint: " + str(url))
    retry_count = 10 
    for retry in range(retry_count):
        print(str(datetime.now()) + " Connecting to Blizzard API. Try: " + str(retry + 1))
        api_result = tryConnetion(url)
        if api_result == None:
            print(str(datetime.now()) + " Sleeping 15s...")
            time.sleep(15)
            continue
        else:
            cards = api_result
            print(str(datetime.now()) + " Success! Insertion in Progress")
            insertIntoDatabase(cards)
            break

