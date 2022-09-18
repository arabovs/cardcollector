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
  "lotr-promotional": "lotr-promotional",
  "": "empty"
}

client = Client(transport=transport, fetch_schema_from_transport=True)

#get price from url, 0 if no valid url
def getPriceFromURL(page_url): 
  page_price_url = requests.get(page_url)
  soup_price = BeautifulSoup(page_price_url.content, "html.parser")
  card_price = soup_price.find(class_='item-price')
  card_price_formatted = cleanPrice(card_price)
  return card_price_formatted

#removes and format's card name
def cleanCardName( card_name ):
  return str(card_name).replace(",","").replace(" ","-").replace("•","").replace("(", "").replace(")", "")

#cleans html tag from span
def cleanPrice( card_price ):
  if card_price is None:
    return 0
  return str(card_price).replace("<span class=\"item-price\">$","").replace("<span class=\"sub-price\">","").replace("</span></span>","")  

#create base url from pricing website
def createNewURL(edition, card_name_cleaned):
  return URL_PRICING + editions_dict[edition] + "/" + card_name_cleaned

#insert row in db pricing table
def gqlInsertCard(card_name, card_edition, card_price, card_price_foil, card_price_tng, source, card_id):
    query = gql("""mutation MyMutation($card_name: String!, $card_edition: String!, $card_price: float8!, $card_price_foil: float8!, $card_price_tng: float8!, $source: String!, $card_id: String!) {
      insert_lotr_all_cards_pricing(objects: {card_name: $card_name,
                                      card_edition: $card_edition,
                                      card_price: $card_price,
                                      card_price_foil: $card_price_foil, 
                                      card_price_tng: $card_price_tng,
                                      card_id: $card_id,
                                      source: $source 
                                      }) {
        affected_rows
      }
    }""")

    params = {
        "card_name": card_name,
        "card_edition": card_edition,
        "card_price": card_price,
        "card_price_foil": card_price_foil,
        "card_price_tng": card_price_tng,
        "card_id": card_id,
        "source": source
    }
    result = client.execute(query, variable_values=params)
    
    #insert row in db pricing table
def gqlFindCardbyName(card_name):
    query = gql("""query MyQuery($card_name: String!) {
      lotr_all_cards_pricing(where: {card_name: {_ilike: $card_name}}) {
            id
            card_name
            card_price
            card_price_foil
            card_price_tng
      }
    }""")
 
    params = {
        "card_name": ("%"+card_name+"%"),
    }
    result = client.execute(query, variable_values=params)
    return result


# PROCESS START

print("Process Start:", now.strftime("%d/%m/%Y %H:%M:%S"))

def scrapeLatestPricing():
    cards_table = soup.find_all('table', class_='inline') 
    for cards in cards_table:
        rows = cards.find_all('tr')
        for row in rows:
            card_id = str(row.find('td').string)
            card_name_cleaned = cleanCardName(card_name = row.find('td', class_= 'col1').string)       
            card_id_regex_number = re.compile(r"^([^a-zA-Z]*)") #Monk code kepp
            edition = re.search(card_id_regex_number, card_id).group(0)
    
            # skipping here as we need to handle promo cards better
            if  "Title" in card_name_cleaned:
              print("Skipping: " + card_name_cleaned)
              continue
            
            URL_PRICE = createNewURL(edition, card_name_cleaned)
            
            card_price      = getPriceFromURL(URL_PRICE) 
            card_price_foil = getPriceFromURL(URL_PRICE + "-foil") 
            card_price_tng  = getPriceFromURL(URL_PRICE + "-tengwar")
           
              
            print(f"Inserting Card Name: " + card_name_cleaned + " with regular price of: " + str(card_price) + " and foil price: " + str(card_price_foil) + " and tengwar price: " + str(card_price_tng))
            gqlInsertCard(str(row.find('td', class_= 'col1').string).replace("•",""),editions_dict[edition].replace(" ","-"),card_price, card_price_foil, card_price_tng,  source,str(row.find('td').string))



def printCardByName(card_name):
    data = gqlFindCardbyName(card_name)
    for array in data["lotr_all_cards_pricing"]:
      print(array["card_price"])
    

def openFile(input_filename):
  f = open(input_filename, "r")
  for x in f:
     printCardByName(x.replace("\n",""))



#### THIS WHERE ALL MAGIC LIES :D #####
openFile("test/input.test")
#scrapeLatestPricing()
  
print("Process End:", now.strftime("%d/%m/%Y %H:%M:%S"))





#### THIS WHERE ALL MAGIC LIES :D #####