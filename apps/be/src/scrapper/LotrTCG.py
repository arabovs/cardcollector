from operator import concat
from requests import request
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from GQL import GQL
from etc import etc
import re

source = "ccgcastle"
URL = "https://lotrtcgwiki.com/wiki/grand" 
URL_PRICING = "https://www.ccgcastle.com/product/lotr-tcg/" 
list_char = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','y','x','z']

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
now = now = datetime.now()

# src/GQL.py
gql_connector = GQL()

# src/etc.py
editions_dict = etc().editions_dict

#get price from url, 0 if no valid url
def getPriceFromURL(page_url): 
  page_price_url = requests.get(page_url)
  soup_price = BeautifulSoup(page_price_url.content, "html.parser")
  card_price = soup_price.find(class_='item-price')
  card_price_formatted = cleanPrice(card_price)
  
  return card_price_formatted

#removes and format's card name
def cleanCardName( card_name ):
  card = str(card_name).replace(",","").replace(" ","-").replace("•","").replace("(", "").replace(")", "").replace("!", "").replace(".","").replace("'","-")
  if card[-1] == 'T':
   card = re.sub(r".$", "tengwar", card)

  return card
#cleans html tag from span
def cleanPrice( card_price ):
  if card_price is None:
    return 0
  return str(card_price).replace("<span class=\"item-price\">$","").replace("<span class=\"sub-price\">","").replace("</span></span>","")  

#create base url from pricing website
def createNewURL(edition, card_name_cleaned):
  return URL_PRICING + editions_dict[edition] + "/" + card_name_cleaned

#used to obtain other info for card
def cardURLgenerator(card_edition, card_number):
  if len(card_edition) == 1:
    card_edition = concat("0",card_edition)
  if len(card_number) == 1:
    card_number = concat("00",card_number)
  if len(card_number) == 2:
    card_number = concat("0",card_number)
  return concat(card_edition,card_number)

def splitEditionID(id):
    card_edition = 0
    card_number = 0
    position = 0
    for c in list(id):
        if c.lower() in list_char:
            position+=1
            card_edition = id[0:position-1]
            card_number = id[position:len(id)]
        position+=1
    return cardURLgenerator(card_edition, card_number)

def fetchCardDetailsDict(card_url):
  card_details = requests.get(card_url)
  soup_card_details = BeautifulSoup(card_details.content, "html.parser")
  dict = {};  key = 0;  value = 0
  for card_detail_row in soup_card_details.find_all('tr'):
# THIS NEEDS FIXING
   try:
     ## try with BS.tag.strip()
     key = str(card_detail_row.find('td', class_='col0').a.string).lower().replace(" ","_")
     value = card_detail_row.find('td', class_='col1').a.string
     if (str(key) == 'game_text'):
      card_game_text = str(card_detail_row.find('td', class_='col1'))
      card_game_text_formatted = ""
      for e in re.findall(r'>(.*?)<', card_game_text):
        card_game_text_formatted += e
      dict[key] = card_game_text_formatted
     if (str(key) != 'game_text'):
      dict[key] = str(value).lower().replace("<em>","").replace("�","").replace("</em>","")
   except:
     try:
       key = str(card_detail_row.find('td', class_='col0').a.string)
     except:
       print("")
     value = str(card_detail_row.find('td', class_='col1')).replace("<td class=\"col1\"> ","").replace("</td>","")
     if (str(key) != 'game_text'):
        dict[str(key).lower().replace(" ","_")] = re.sub(r"[^a-zA-Z0-9.:;!?,\s+]","",str(value).replace("<em>","").replace("�","").replace("</em>",""))
     
  return dict
# PROCESS START



print("Process Start:", now.strftime("%d/%m/%Y %H:%M:%S"))

def scrapeLatestPricing():
    cards_table = soup.find_all('table', class_='inline')
    increment = 0
    for cards in cards_table:
        rows = cards.find_all('tr')
        for row in rows:
            if increment > 1:
              
              # Basic Card info from Grand Page
              card_id = str(row.find('td').string)
              card_name = str(row.find('td', class_= 'col1').string).replace("•","")
              card_id_regex_number = re.compile(r"^([^a-zA-Z]*)\w+(\d+)") #Monk code keep
              card_edition = re.search(card_id_regex_number, card_id).group(1)
              card_number = re.search(card_id_regex_number, card_id).group(2)
              card_name_cleaned = cleanCardName(card_name = row.find('td', class_= 'col1').string)     
              # DND card_type = str(row.find('td', class_= 'col2').find('a').string)
              # DND card_culture = str(row.find('td', class_= 'col3').find('a').string)
              
              # Detailed Card Info from 
              card_image = "https://lotrtcgwiki.com/wiki/_media/cards:lotr" + splitEditionID(card_id) + ".jpg"
              card_dict = fetchCardDetailsDict("https://lotrtcgwiki.com/wiki/lotr" + splitEditionID(card_id))
              card_dict["card_image"] = card_image
              card_dict["card_name"] = card_name
              card_dict["card_id"] = card_id
              card_dict["card_edition"] = card_edition
              card_dict["card_number"] = card_number
              # DND card_dict["card_type"] = card_type.lower()
              # DND card_dict["card_culture"] = card_culture.lower()
              
              print(json.dumps(str(card_dict),sort_keys=True, indent=4))
              #print(type(card_detail_row.find('td', class_='col1')))
              #soup_card_details.find(class_='item-price')
              # skipping here as we need to handle promo cards better
              if  "Title" in card_name_cleaned:
                print("Skipping: " + card_name_cleaned)
                continue
              URL_PRICE = createNewURL(card_edition, card_name_cleaned)
              card_price      = getPriceFromURL(URL_PRICE) 
              card_price_foil = getPriceFromURL(URL_PRICE + "-foil") 
              card_price_tng  = getPriceFromURL(URL_PRICE + "-tengwar")

              gql_connector.gqlInsertCard( card_dict.get("card_name",""), card_dict.get("card_edition",""), card_price, card_price_foil, card_price_tng, source, card_dict.get("card_id",""), card_dict.get("card_image",""),card_dict.get("kind",""),card_dict.get("culture",""),card_dict.get("twilight",0),card_dict.get("card_type",""),card_dict.get("card_number",""),card_dict.get("lore",""),card_dict.get("game_text","")) 
            increment += 1

scrapeLatestPricing()
  
print("Process End:", now.strftime("%d/%m/%Y %H:%M:%S"))

