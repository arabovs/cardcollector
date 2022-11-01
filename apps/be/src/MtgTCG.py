import requests
import sys
from GQL import GQL

gql_connector = GQL()
url = 'https://api.scryfall.com/cards/search?q=!"smokestack"&unique=prints'
mtg_cards = requests.get(url).json()


# option == 1 for printing card/cards/
# else insert to db
def printInsert(option):
    if option == 1:
        print(card)
    else:
        gql_connector.gqlInsertGenericCard(
                                   "mtg",
                                   card.get("id",""),
                                   card.get("name",""),
                                   card["image_uris"]["normal"],
                                   card.get("set",""),
                                   card.get("collector_number",""),
                                   card.get("rarity",""),
                                )


mtg_cards = requests.get(url).json()

#loop through all cards
for card in mtg_cards["data"]:
    printInsert(2)
    break


