import requests
import sys
from GQL import GQL

gql_connector = GQL()
url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Tornado%20Dragon'
yugioh_cards = requests.get(url).json()
for card in yugioh_cards["data"]:
    print(card)
    print(card["card_images"][0]["image_url"])
    gql_connector.gqlInsertGenericCard("yugioh",
                                   str(card.get("id","")),
                                   card.get("name",""),
                                   card["card_images"][0]["image_url"],
                                   card["card_sets"][0]["set_name"],
                                   card["card_sets"][0]["set_code"],
                                   card["card_sets"][0]["set_rarity_code"],
                                )
    break

