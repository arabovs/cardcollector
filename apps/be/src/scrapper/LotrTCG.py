from operator import concat
from requests import request
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from GQL import GQL
from etc import etc
import re

source = "ccgcastle"
URL = "https://lotrtcgwiki.com/wiki/grand" 
URL_PRICING = "https://www.ccgcastle.com/product/lotr-tcg/" 

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
now = now = datetime.now()

# src/GQL.py
gql_connector = GQL()

# src/etc.py
editions_dict = etc().editions_dict


def getImageFromURL(page_url, card_id):
  return ""
  image_url = requests.get(page_url)
  soup_img = BeautifulSoup(image_url.content, "html.parser")
  card_img = soup_img.find(id = "product-image")
  site_url = "https://www.ccgcastle.com"

  try:
    img = card_img['src'] 
    img_url = site_url + img
  except:
    if page_url[-1] == 'D':
      img_url = getImageFromURL(page_url.replace("-D",""), card_id)
      print(img_url)
    if page_url[-1] == 'P':
      new_page_url = re.sub(r".$", card_id, page_url)
      img_url = getImageFromURL(new_page_url, card_id)
  return img_url

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

def fetchCardDetailsDict(card_url):
  card_details = requests.get(card_url)
  soup_card_details = BeautifulSoup(card_details.content, "html.parser")
  dict = {};  key = 0;  value = 0
  for card_detail_row in soup_card_details.find_all('tr'):
# THIS NEEDS FIXING
   try:
     key = card_detail_row.find('td', class_='col0').a.string
     value = card_detail_row.find('td', class_='col1').a.string
     dict[str(key).lower().replace(" ","_")] = str(value).lower()
   except:
     try:
       key = str(card_detail_row.find('td', class_='col0').a.string)
     except:
       print("")
     value = str(card_detail_row.find('td', class_='col1')).replace("<td class=\"col1\"> ","").replace("</td>","")
     dict[str(key).lower().replace(" ","_")] = str(value).lower()
     
  return dict
# PROCESS START

print("Process Start:", now.strftime("%d/%m/%Y %H:%M:%S"))

def scrapeLatestPricing():
    cards_table = soup.find_all('table', class_='inline')
    increment = 0
    for cards in cards_table:
        rows = cards.find_all('tr')
        for row in rows:
            if increment > 200 and increment < 250:
              
              # Basic Card info from Grand Page
              card_id = str(row.find('td').string)
              card_name = str(row.find('td', class_= 'col1').string).replace("•","")
              card_id_regex_number = re.compile(r"^([^a-zA-Z]*)\w+(\d+)") #Monk code kepp
              card_edition = re.search(card_id_regex_number, card_id).group(1)
              card_number = re.search(card_id_regex_number, card_id).group(2)
              card_name_cleaned = cleanCardName(card_name = row.find('td', class_= 'col1').string)     
              # DND card_type = str(row.find('td', class_= 'col2').find('a').string)
              # DND card_culture = str(row.find('td', class_= 'col3').find('a').string)
              
              # Detailed Card Info from 
              #print("https://lotrtcgwiki.com/wiki/lotr" + cardURLgenerator(card_edition,card_number))
              card_dict = fetchCardDetailsDict("https://lotrtcgwiki.com/wiki/lotr" + cardURLgenerator(card_edition,card_number))
              card_dict["card_name"] = card_name
              card_dict["card_id"] = card_id
              card_dict["card_edition"] = card_edition
              card_dict["card_number"] = card_number
              # DND card_dict["card_type"] = card_type.lower()
              # DND card_dict["card_culture"] = card_culture.lower()
              
              print(str(increment) + " " + str(card_dict))
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
              card_image      = getImageFromURL(URL_PRICE, card_id) 
              print("HEY: " + card_dict["card_id"])
              #print(URL_PRICE)
              #print(card_image)
              #gql_connector.gqlInsertCard(str(row.find('td', class_= 'col1').string).replace("•",""),editions_dict[edition].replace(" ","-"),card_price, card_price_foil, card_price_tng,  source,str(row.find('td').string), str(card_image))
              #print(f"Inserting Card " + str(increment) + " Name: " + card_name_cleaned + " with regular price of: " + str(card_price) + " and foil price: " + str(card_price_foil) + " and tengwar price: " + str(card_price_tng))
              #gqlInsertCard(self, card_name, card_edition, card_price, card_price_foil, card_price_tng, source, card_id, card_img,card_kind,card_culture,card_twilight,card_type,card_number):
              gql_connector.gqlInsertCard( card_dict.get("card_name",""), card_dict.get("card_edition",""), 0, 0, 0, source, card_dict.get("card_id",""), "",card_dict.get("kind",""),card_dict.get("culture",""),card_dict.get("twilight",0),card_dict.get("card_type",""),card_dict.get("card_number","")) 
            increment += 1

scrapeLatestPricing()
  
print("Process End:", now.strftime("%d/%m/%Y %H:%M:%S"))

