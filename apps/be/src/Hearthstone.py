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
url_card = f"https://us.api.blizzard.com/hearthstone/cards/52119-arch-villain-rafaam?locale=en_US&gameMode=%22constructed%22&access_token={access_token}"

print(url_card)
card = requests.get(url_card).json()
print(card)

gql_connector.gqlInsertGenericCard(
            "hearthstone",
            str(card.get("slug","")),
            card.get("name",""),
            card.get("imageGold",""),
            str(card.get("cardTypeId","")),
            str(card.get("cardSetId","")),
            str(card.get("cardSetId","")),
            str(card.get("rarityId","")),
            None,
            None,
            None,
            str(card.get("cardTypeId","")),
            None,
            str(card.get("text","")),
            str(card.get("flavorText","")),
            str(card.get("manaCost","")),
            None,
            str(card.get("attack","")),
            str(card.get("health","")),
            None
        )

print("inserted")

