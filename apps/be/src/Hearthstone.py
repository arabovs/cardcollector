import requests
import json

from etc.postgre.GQL import GQL
from etc.hearthstone.metadata import metadata

#print(metadata["types"])
#print(metadata["rarities"])
#print(metadata["classes"])
#print(metadata["minionTypes"])
#print(metadata["keywords"])
id = 1



AUTH_URL = 'https://oauth.battle.net/token'

URL_CARD = f"https://us.api.blizzard.com/hearthstone/cards?locale=en_US"

# METADATA
# URL_CARD = f"https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token={access_token}"
# URL_CARD = f"https://us.api.blizzard.com/hearthstone/metadata/sets?locale=en_US"
# URL_CARD = f"https://us.api.blizzard.com/hearthstone/metadata/classes?locale=en_US&access_token={access_token}"
# URL_CARD = f"https://us.api.blizzard.com/hearthstone/metadata/keywords?locale=en_US&access_token={access_token}"


gql_connector = GQL() # initialise postgre connector


# Get token from Blizzard's AUTH_URL
def getAuthToken():
    params = {
        'client_secret': 'pd6Ig2jOWTKAg0F5svIdT7wX3iajDqMN',
        'grant_type': 'client_credentials',
        'client_id': '7af929a351344362909d803901df5897',
    }

    print("getting access Token")
    response = requests.post(AUTH_URL, data=params)
    access_token = json.loads(response.text.replace("'", "\""))["access_token"]
    return access_token

# Fetch JSON from Blizzard's endpoint
def getJSONfromApi(access_token, endpoint):
    cards = requests.get(endpoint + "\&access_token=" + access_token).json()
    return cards

# takes a card objects and cleans various fields as per db model
def cleanupCard(card):
    
    # clean up cardTypeId
    if "cardTypeId" in card:
        for type in metadata["types"]:
            for key, value in type.items():
                if key == "id" and value == card["cardTypeId"]:
                    card["cardTypeId"] = type["name"]
                    break
    else:
        card["cardTypeId"] = None
    
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

def insertIntoDatabase(cards):
    i=0 # used for debug purposes
    #for card in cards: # for metadata
    for card in cards["cards"]: # for all cards
        card = cleanupCard(card)
        gql_connector.gqlInsertGenericCard(
                "hearthstone",
                str(card.get("slug","")),
                card.get("name",""),
                card.get("image",""),
                str(card.get("cardTypeId",None)),
                str(card.get("cardSetId",None)),
                str(card.get("cardSetId",None)),
                str(card.get("rarityId",None)),
                None,
                None,
                None,
                str(card.get("cardTypeId",None)),
                None, # minions array
                card.get("text",None),
                card.get("flavorText",None),
                card["manaCost"],
                None,
                card["attack"],
                card["health"],
                None
        )
        i+=1 
    print("Inserted " + str(i))

    
insertIntoDatabase(getJSONfromApi(getAuthToken(), URL_CARD))

