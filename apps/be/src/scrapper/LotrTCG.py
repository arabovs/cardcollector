from requests import request
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from GQL import GQL
from etc import etc
from ErrorHandle import ErrorHandle
import re

source = "ccgcastle"
URL = "https://lotrtcgwiki.com/wiki/grand" 
URL_PRICING = "https://www.ccgcastle.com/product/lotr-tcg/" 
card_back_img = "https://www.ccgcastle.com/product/lotr-tcg/lotr-complete-sets/mines-of-moria-complete-set" #for missing cards

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
now = now = datetime.now()

# src/GQL.py
gql_connector = GQL()

# src/etc.py
editions_dict = etc().editions_dict

#src/ErrorHandle.py
error_handle = ErrorHandle()


def getImageFromURL(page_url, card_id):

  page_url = ErrorHandle.check_URL(page_url)

  image_url = requests.get(page_url)
  soup_img = BeautifulSoup(image_url.content, "html.parser")
  card_img = soup_img.find(id = "product-image")
  site_url = "https://www.ccgcastle.com"

  print(page_url)

  try:
    img = card_img['src'] 
    img_url = site_url + img
    
  except:
    

    if page_url[-1] == 'D':
      img_url = getImageFromURL(page_url.replace("-D",""), card_id)
      #print(img_url)

    if page_url[-1] == 'M':
      img_url = getImageFromURL(page_url.replace("-M",""), card_id)
      #print(img_url)  
    
    if page_url[-1] == 'P':
      new_page_url = re.sub(r".$", card_id, page_url)
      img_url = getImageFromURL(new_page_url, card_id)

    if page_url[-8:] == "-tengwar":
      new_page_url = page_url.replace("-tengwar","-t")
      img_url = getImageFromURL(new_page_url, card_id)

    
    
  return img_url

#get price from url, 0 if no valid url
def getPriceFromURL(page_url): 
  page_url = ErrorHandle.check_URL(page_url)

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

# PROCESS START

print("Process Start:", now.strftime("%d/%m/%Y %H:%M:%S"))

def scrapeLatestPricing():
    cards_table = soup.find_all('table', class_='inline')
    increment = 0
    for cards in cards_table:
        rows = cards.find_all('tr')
        for row in rows:
            if increment > 874 and increment < 5000:
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
              print(card_id)
              card_image      = getImageFromURL(URL_PRICE, card_id) 

              print(URL_PRICE)
              print(card_image)
              #gql_connector.gqlInsertCard(str(row.find('td', class_= 'col1').string).replace("•",""),editions_dict[edition].replace(" ","-"),card_price, card_price_foil, card_price_tng,  source,str(row.find('td').string), str(card_image))
              #print(f"Inserting Card " + str(increment) + " Name: " + card_name_cleaned + " with regular price of: " + str(card_price) + " and foil price: " + str(card_price_foil) + " and tengwar price: " + str(card_price_tng))

            increment += 1

scrapeLatestPricing()
  
print("Process End:", now.strftime("%d/%m/%Y %H:%M:%S"))

