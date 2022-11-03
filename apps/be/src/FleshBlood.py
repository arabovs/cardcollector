import requests
import sys
from GQL import GQL

#%20

gql_connector = GQL() 

#https://api.gwentapi.com/v0?
urls = [
        'https://api.fabdb.net/cards?time=1662853301',
    ]

def cardSearch(url):
    fb_cards = requests.get(url).json()
    
    for card in fb_cards["data"]:
        print(card)
        
for url in urls:        
    cardSearch(url)