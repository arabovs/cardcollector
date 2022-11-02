import requests
import sys
from GQL import GQL

#%20

gql_connector = GQL() 
urls = [
        'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Pot%20Of%20Greed',
        'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark%20Magician',
        'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark%20Magician%20Girl',
        'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Mystic%20Tomato',
        'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Beaver%20Warrior',
        'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Kuriboh',
        'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Morphing%20Jar',
        'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Man-Eater%20Bug',
    ]

def cardSearch(url):
    def printInsert(option):
        if option ==1:
            print(card)

        else:
            set_codes = card["card_sets"][0]["set_code"].split("-")
            set_code = set_codes[0]
            set_id   = set_codes[1]      
                 
            gql_connector.gqlInsertGenericCard("yugioh",
                                           str(card.get("id","")),
                                           card.get("name",""),
                                           card["card_images"][0]["image_url"],
                                           card["card_sets"][0]["set_name"],
                                           set_code,
                                           set_id,
                                           card["card_sets"][0]["set_rarity_code"].replace("(","").replace(")","").title(),
                                           card["card_prices"][0]["cardmarket_price"],
                                           card["card_prices"][0]["tcgplayer_price"],
                                           card["card_prices"][0]["ebay_price"],
                                           card["type"],
                                           card["race"],
                                           card["desc"],
                                           "",
                                           )


    yugioh_cards = requests.get(url).json()
    for card in yugioh_cards["data"]:
        printInsert(2)


for url in urls:
    cardSearch(url)