import requests
import sys
from GQL import GQL

gql_connector = GQL()
url = 'https://api.scryfall.com/cards/search?q=!"thoughtseize"&unique=prints'
mtg_cards = requests.get(url).json()
for card in mtg_cards["data"]:

    gql_connector.gqlInsertGenericCard("mtg",
                                   card.get("id",""),
                                   card.get("name",""),
                                   card["image_uris"]["normal"],
                                   card.get("set",""),
                                   card.get("collector_number",""),
                                   card.get("rarity",""),
                                )
    break

