import requests
import json
import time

from etc.postgre.GQL import GQL
from etc.hearthstone.metadata import metadata

AUTH_URL = 'https://oauth.battle.net/token'


url_pages = [
#"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&pageSize=500",
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
        'client_secret': 'pd6Ig2jOWTKAg0F5svIdT7wX3iajDqMN',
        'grant_type': 'client_credentials',
        'client_id': '7af929a351344362909d803901df5897',
    }

    print("Getting Access Token...")
    response = requests.post(AUTH_URL, data=params)
    access_token = json.loads(response.text.replace("'", "\""))["access_token"]
    print("Access Token: " + access_token)
    return access_token

# Fetch JSON from Blizzard's endpoint
def getJSONfromApi(access_token, endpoint):
    cards = requests.get(endpoint + "\&access_token=" + access_token).json()
    return cards

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
    print("Inserting cards")
    #for card in cards: # for metadata
    for card in cards["cards"]: # for all cards
        card = cleanupCard(card) # clean up required for all cards as part standartization
        gql_connector.gqlInsertGenericCard(
                "hearthstone",
                str(card.get("slug","")),
                card.get("name",""),
                card.get("image",""),
                str(card.get("cardSetId",None)),
                str(card.get("cardSetIdOld","")),
                str(card.get("id",None)),
                str(card.get("rarityId",None)),
                None,
                None,
                None,
                str(card.get("cardTypeId",None)),
                card.get("minionTypeId",None), 
                card.get("text",None),
                card.get("flavorText",None),
                card["manaCost"],
                None,
                card["attack"],
                card["health"],
                card.get("classId",None),
        )

# loops through pages of 500 cards
for url in url_pages:
    insertIntoDatabase(getJSONfromApi(getAuthToken(), url))
    print("Cards Inserted")
    time.sleep(60)

