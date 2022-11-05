import requests
import json

URL_GWEN = "https://api.gwent.one/?key=data&version=1.0.0.15"
gwent_cards = requests.get(URL_GWEN).json()
print(gwent_cards)