from requests import request
import requests
from gql import Client, gql
from bs4 import BeautifulSoup
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import re


source = "ccgcastle"
URL = "https://lotrtcgwiki.com/wiki/grand" 
URL_PRICING = "https://www.ccgcastle.com/product/lotr-tcg/" 
HASURA_URL = "https://lotrtcgwebscrapper.herokuapp.com/v1/graphql"

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
now = now = datetime.now()

transport = RequestsHTTPTransport(
    url=HASURA_URL,
    verify=True,
    retries=3,
)

# todo: will be used in the promo handling logic
name_dic = {
  "-(D)":"",
  "-(T)":"",
  "-(AFD)":"",
  "-(P)":"",
  "-(W)":"",
  "-(M)":"",
}

# used for translating edition code to url path
editions_dict = {
  "1": "The-Fellowship-of-the-Ring",
  "2": "Mines-of-Moria",
  "3": "Realms-of-the-Elf-lords",
  "4": "The-Two-Towers",
  "5": "Battle-of-helms-deep",
  "6": "Ents-of-Fangorn",
  "7": "Battle-of-Helms-Deep",
  "8": "The-Return-of-the-King",
  "9": "Siege-of-Gondor", 
  "10": "Reflections",
  "11": "Mount-Doom",
  "12": "Shadows",
  "13": "Black-Rider",
  "14": "Bloodlines",
  "15": "Expanded-Middle-earth",
  "16": "The-Hunters",
  "17": "The-Wraith-Collection",
  "18": "Rise-of-Saruman", 
  "19": "Treachery-and-Deceit",
  "0": "lotr-promotional",
  "": "empty"
}

client = Client(transport=transport, fetch_schema_from_transport=True)

def cleanCardName( card_name ):
  return str(card_name).replace(",","").replace(" ","-").replace("•","")

def cleanPrice( card_price ):
  return str(card_price).replace("<span class=\"item-price\">$","").replace("<span class=\"sub-price\">","").replace("</span></span>","")  

def createNewURL(edition, card_name_cleaned):
  return URL_PRICING + editions_dict[edition] + "/" + card_name_cleaned

def runGQL(card_name, card_edition, card_price, source):
    query = gql("""mutation MyMutation($card_name: String!, $card_edition: String!, $card_price: float8!, $source: String!) {
      insert_lotr_all_cards_pricing(objects: {card_name: $card_name,
                                      card_edition: $card_edition,
                                      card_price: $card_price,
                                      source: $source 
                                      }) {
        affected_rows
      }
    }""")

    params = {
        "card_name": card_name,
        "card_edition": card_edition,
        "card_price": card_price,
        "source": source
    }
    result = client.execute(query, variable_values=params)


# PROCESS START

print("Process Start:", now.strftime("%d/%m/%Y %H:%M:%S"))

cards_table = soup.find_all('table', class_='inline') 

for cards in cards_table:
    rows = cards.find_all('tr')
    for row in rows:
        card_id = str(row.find('td').string)
        card_name_cleaned = cleanCardName(card_name = row.find('td', class_= 'col1').string)
        card_id_regex = re.compile(r"^([^a-zA-Z]*)")
        edition = re.search(card_id_regex, card_id).group(0)
        
        # skipping here as we need to handle promo cards better
        if edition == '0' or "("  in card_name_cleaned or "Title" in card_name_cleaned:
          print("Skipping: " + card_name_cleaned)
          continue
        
        URL_PRICE = createNewURL(edition, card_name_cleaned)
        page_price = requests.get(URL_PRICE)
        soup_price = BeautifulSoup(page_price.content, "html.parser")
        card_price = soup_price.find(class_='item-price')
        card_price_formatted  = cleanPrice(card_price)
        
        print("Inserting " + card_name_cleaned + " price: " + card_price_formatted)
        
        # Insert into postGre
        if card_price_formatted != "None":
          runGQL(card_name_cleaned,editions_dict[edition].replace(" ","-"),card_price_formatted, source)


# PROCESS END
print("Process End:", now.strftime("%d/%m/%Y %H:%M:%S"))