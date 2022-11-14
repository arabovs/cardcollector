import requests
import sys
from etc.postgre.GQL import GQL

#%20

gql_connector = GQL() 

#https://api.gwentapi.com/v0?
urls = [
        #'https://api.fabdb.net/cards?per_page=100&page=1',
        'https://api.fabdb.net/cards?per_page=100&page=2',
        'https://api.fabdb.net/cards?per_page=100&page=3',
        'https://api.fabdb.net/cards?per_page=100&page=4',
        'https://api.fabdb.net/cards?per_page=100&page=5',
        'https://api.fabdb.net/cards?per_page=100&page=6',
        'https://api.fabdb.net/cards?per_page=100&page=7',
    ]

def cardSearch(url):
    fb_cards = requests.get(url).json()
    i = 0
    for card in fb_cards["data"]:
        #print(card)
        if i > 10:
            break
        cost_cleaned = None
        if "stats" in card.keys():
            if "cost" in card["stats"]:
                cost_cleaned = card["stats"]["cost"]
                
        attack_cleaned = None        
        if "stats" in card.keys():
            if "attack" in card["stats"]:
                attack_cleaned = card["stats"]["attack"]
                
        defense_cleaned = None        
        if "stats" in card.keys():
            if "defense" in card["stats"]:
                defense_cleaned = card["stats"]["defense"]
        
        resource_cleaned = None   
        if "stats" in card.keys():
            if "resource" in card["stats"]:
                resource_cleaned = card["stats"]["resource"]
        
        text_cleaned = ""    
        keywords_cleaned = ""
        if "keywords" in card.keys():
            for keyword in card["keywords"]:
                keywords_cleaned = "[" + keyword + "]"
        
        if "text" in card.keys():
            keywords_cleaned = card["text"]

        game_text = keywords_cleaned + text_cleaned
        if game_text == "":
            game_text = None
        
        for y in range(len(card["printings"])):
            gql_connector.gqlInsertGenericCard(
                              "fnb",
                               str(card["identifier"]),
                               card["name"],
                               card["printings"][y]["image"],
                               card["printings"][y]["sku"]["set"]["name"],
                               str(card["printings"][y]["sku"]["set"]["id"]),
                               str(card["printings"][y]["id"]),
                               card["rarity"],
                               None,
                               None,
                               None,
                               None,
                               None,
                               game_text,
                               card["printings"][y]["flavour"],
                               resource_cleaned,
                               None,
                               attack_cleaned, #
                               defense_cleaned, 
                               None,
                               None,
                               None,
                               None,
                               None,
                               None,
                               None,
                            )
        
for url in urls:        
    cardSearch(url)