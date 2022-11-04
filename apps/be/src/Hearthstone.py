import requests
from GQL import GQL
import json
#from blizzardapi import BlizzardApi
gql_connector = GQL() 

url = 'https://oauth.battle.net/token'

params = {
    'client_secret': 'pd6Ig2jOWTKAg0F5svIdT7wX3iajDqMN',
    'grant_type': 'client_credentials',
    'client_id': '7af929a351344362909d803901df5897',
}

print("getting access Token")
response = requests.post(url, data=params)
access_token = json.loads(response.text.replace("'", "\""))["access_token"]

# gets 40 cards for some reason
# url_card = f"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token={access_token}"

# METADATA
url_card = f"https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token={access_token}"
# url_card = f"https://us.api.blizzard.com/hearthstone/metadata/sets?locale=en_US&access_token={access_token}"
# url_card = f"https://us.api.blizzard.com/hearthstone/metadata/classes?locale=en_US&access_token={access_token}"
# url_card = f"https://us.api.blizzard.com/hearthstone/metadata/keywords?locale=en_US&access_token={access_token}"



cards = requests.get(url_card).json()
print(cards)
for card in cards: # for metadata
#for card in cards["cards"]: # for all cards
        print(card["id"],card["name"])
        #print("ID "+ str(card["id"]) + " name: " + card["name"] +" : " + card["text"])
        
        # clean up attack and health
        #attack_cleaned = None
        #if "attack" in card.keys():
        #    attack_cleaned = float(card["attack"])
        #    
        #health_cleaned = None
        #if "attack" in card.keys():
        #    health_cleaned = float(card["health"])

        ## mana cost clean up
        #mana_cleaned = None
        #if "manaCost" in card.keys():
        #    mana_cleaned = card["manaCost"]
        
        #gql_connector.gqlInsertGenericCard(
        #        "hearthstone",
        #        str(card.get("slug","")),
        #        card.get("name",""),
        #        card.get("image",""),
        #        str(card.get("cardTypeId",None)),
        #        str(card.get("cardSetId",None)),
        #        str(card.get("cardSetId",None)),
        #        str(card.get("rarityId",None)),
        #        None,
        #        None,
        #        None,
        #        str(card.get("cardTypeId",None)),
        #        None,
        #        card.get("text",None),
        #        card.get("flavorText",None),
        #        mana_cleaned,
        #        None,
        #        attack_cleaned,
        #        health_cleaned,
        #        None
        #    )

print("inserted")

