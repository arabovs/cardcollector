import requests
import sys
from etc.postgre import GQL

#%20

gql_connector = GQL() 

#https://api.gwentapi.com/v0?
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

            
    yugioh_cards = requests.get(url).json()
    i = 1
    for card in yugioh_cards["data"]:           
        # Card sets - some cards have [] others {} and some None ( we skip in this case)
        if "card_sets" not in card.keys():
            print("Skipping " + str(i))
            i+=1
            continue
        for y in range(len(card["card_sets"])):
            print(card)
            set_codes = None
            if card["card_sets"] is list:
                set_codes = card["card_sets"][y]
            else:
                set_codes = card["card_sets"]

            set_codes = card["card_sets"][y]["set_code"].split("-")
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

            card_atk_cleaned = None
            if "atk" in card.keys():
                if card["atk"] is not None:
                    card_atk_cleaned = float(card["atk"])

            card_def_cleaned = None
            if "def" in card.keys():
                if card["def"] is not None:
                    card_def_cleaned = float(card["def"])

            print("Inserted " + str(i)) 
            i += 1 
            gql_connector.gqlInsertGenericCard(
                                                "yugioh",
                                                str(card.get("id","")),
                                                card.get("name",""),
                                                card["card_images"][0]["image_url"],
                                                card["card_sets"][y]["set_name"],
                                                set_code,
                                                set_id,
                                                card["card_sets"][y]["set_rarity_code"].replace("(","").replace(")","").title(),
                                                card["card_prices"][0]["cardmarket_price"],
                                                card["card_prices"][0]["tcgplayer_price"],
                                                card["card_prices"][0]["ebay_price"],
                                                card["type"],
                                                card["race"],
                                                game_text_cleaned,
                                                flavor_text_cleaned,
                                                level_cleaned,
                                                str(level_cleaned),
                                                card_atk_cleaned,
                                                card_def_cleaned,
                                                card.get("archetype",None)
                                                )
                               
for url in urls:
    cardSearch(url)