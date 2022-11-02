import requests
import sys
from GQL import GQL

#%20

gql_connector = GQL() 


urls = [
        'https://db.ygoprodeck.com/api/v7/cardinfo.php',
        #'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Pot%20Of%20Greed',
        #'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark%20Magician',
        #'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark%20Magician%20Girl',
        #'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Mystic%20Tomato',
        #'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Beaver%20Warrior',
        #'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Kuriboh',
        #'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Morphing%20Jar',
        #'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Man-Eater%20Bug',
    ]

def cardSearch(url):
    def printInsert(option):
        if option ==1:
            print(card)

        else:
            # Card sets - some cards have [] others {} and some None ( we return in this case)
            if "card_sets" not in card.keys():
                return
            set_codes = None
            if card["card_sets"] is list:
                set_codes = card["card_sets"][0]
            else:
                set_codes = card["card_sets"]
            
            set_codes = card["card_sets"][0]["set_code"].split("-")
            set_code = set_codes[0]
            set_id   = set_codes[1]
             
            # GAME TEXT and FLAVOR TEXT clean
            game_text_cleaned = ''
            flavor_text_cleaned = ''
            if card["desc"][0:2] == "''":
               game_text_cleaned = None
               flavor_text_cleaned = card["desc"]
            else:
               game_text_cleaned = card["desc"]
               flavor_text_cleaned = None
               
            # LEVEL cleanup  
            level_cleaned = ""
            if "level" not in card.keys():
                level_cleaned = 0
            else:
                level_cleaned = card["level"]
                
                 
            gql_connector.gqlInsertGenericCard(
                                            "yugioh",
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
                                            game_text_cleaned,
                                            flavor_text_cleaned,
                                            level_cleaned,
                                            str(level_cleaned),
                                            float(card.get("atk",0)),
                                            float(card.get("def",0)),
                                        )

    yugioh_cards = requests.get(url).json()
    for card in yugioh_cards["data"]:
        printInsert(2)


for url in urls:
    cardSearch(url)