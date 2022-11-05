from operator import concat
from urllib import response
from requests import request
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from etc.postgre import GQL
from etc.lotrtcg.metadata import HsMetadata
import subprocess
import re
from os.path  import basename

source = "ccgcastle"
URL = "https://lotrtcgwiki.com/wiki/grand" 
URL_PRICING = "https://www.ccgcastle.com/product/lotr-tcg/" 

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
now = now = datetime.now()

# src/GQL.py
gql_connector = GQL()

# src/etc.py
editions_dict = HsMetadata().editions_dict
rarity_dict = HsMetadata().rarity_dict

#get price from url, 0 if no valid url
def getPriceFromURL(page_url): 
  page_price_url = requests.get(page_url)
  soup_price = BeautifulSoup(page_price_url.content, "html.parser")
  card_price = soup_price.find(class_='item-price')
  if card_price is not None:
    card_price_formatted = cleanPrice(card_price)
    return card_price_formatted
  else:
    return 0

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
def cardURLgenerator(set, card_number):
  if len(set) == 1:
    set = concat("0",set)
  if len(card_number) == 1:
    card_number = concat("00",card_number)
  if len(card_number) == 2:
    card_number = concat("0",card_number)
  return concat(set,card_number)

def splitEditionID(id,option):
  if option == 1:
    set = 0
    card_number = 0
    position = 0
    for c in list(id):
        if c.lower().isalpha():
            position+=1
            set = id[0:position-1]
            card_number = id[position:len(id)]
        position+=1
    return cardURLgenerator(set, card_number)
  if option == 2:
    card_number = id[-1:]
    return "00SPD" + card_number
  if option == 3:
    return id.replace("RF","F")
  return
    

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
     if (str(key) == "card_type"):
       card_type = str(card_detail_row.find('td', class_='col1'))
       card_type_combined = ""
       for e in re.findall(r'>(.*?)<', card_type):
         card_type_combined = card_type_combined + e
        
       card_type_combined = re.sub('[^0-9a-zA-Z \'!.?,]+', '', card_type_combined)
       if len(card_type_combined.replace("  ",",").split(",")) == 3:
        dict[key] = card_type_combined.replace("  ",",").split(",")[0]
        dict["home_site"] = card_type_combined.replace("  ",",").split(",")[1] 
        dict["subtype"] = card_type_combined.replace("  ",",").split(",")[2] 
       if len(card_type_combined.replace("  ",",").split(",")) == 2:
        dict[key] = card_type_combined.replace("  ",",").split(",")[0]
        dict["subtype"] = card_type_combined.replace("  ",",").split(",")[1] 
       if len(card_type_combined.replace("  ",",").split(",")) == 1:
        dict[key] = card_type_combined.replace("  ",",").split(",")[0]
       
     if (str(key) == 'lore'):
       card_lore = str(card_detail_row.find('td', class_='col1'))
       card_lore_combined = ""
       for e in re.findall(r'>(.*?)<', card_lore):
         card_lore_combined =  card_lore_combined + e
       card_lore_combined = re.sub('[^0-9a-zA-Z \'!.?,]+', '', card_lore_combined)
       dict[key] = card_lore_combined
       
     if (str(key) == 'game_text'):
      card_game_text = str(card_detail_row.find('td', class_='col1'))
      card_game_text_formatted = ""
      for e in re.findall(r'>(.*?)<', card_game_text):
        card_game_text_formatted += e
      dict[key] = card_game_text_formatted.replace("�","")
      
     if (str(key) not in ['game_text','lore',"card_type"]):
      dict[key] = str(value).lower().replace("<em>","").replace("�","").replace("</em>","")
      
   except:     
     try:
       key = str(card_detail_row.find('td', class_='col0').a.string)
     except:
       print("")
     value = str(card_detail_row.find('td', class_='col1')).replace("<td class=\"col1\"> ","").replace("</td>","")
     
     if (str(key) not in  ['game_text','lore','card_type']):
        dict[str(key).lower().replace(" ","_")] = re.sub(r"[^a-zA-Z0-9.:;!?,\s+]","",str(value).replace("<em>","").replace("�","").replace("</em>",""))
     
  return dict

print("Process Start:", now.strftime("%d/%m/%Y %H:%M:%S"))

def scrapeLatestPricing():
    cards_table = soup.find_all('table', class_='inline')
    i = 0
    for cards in cards_table:
        rows = cards.find_all('tr')
        for row in rows:
            if i > 0:
              # Basic Card info from Grand Page
              card_id = str(row.find('td').string)
              card_name = str(row.find('td', class_= 'col1').string).replace("•","")
              card_id_regex_number = re.compile(r"^([^a-zA-Z]*)\w+(\d+)") 
              card_name_cleaned = cleanCardName(card_name = row.find('td', class_= 'col1').string) 
              
              # Detailed Card Info from - we need to handle SPD and rest better  
              if "(AI)" in card_name_cleaned:
                print("Skipping: " + card_name_cleaned)
                i+=1
                continue      
              if "S" in card_id:
                print("Skipping: " + card_name_cleaned)
                i+=1
                continue            

              set = ""
              card_number = ""
              if "+" not in str(card_id) and card_id[-1].isnumeric():
                set = re.search(card_id_regex_number, card_id).group(1)
                card_number = re.search(card_id_regex_number, card_id).group(2)
                card_name_cleaned.replace("+","")
                if card_name_cleaned[-3:] not in ("SPD"):
                  card_image = "https://lotrtcgwiki.com/wiki/_media/cards:lotr" + splitEditionID(card_id,1) + ".jpg"
                  card_dict = fetchCardDetailsDict("https://lotrtcgwiki.com/wiki/lotr" + splitEditionID(card_id,1))
                elif "RF" in card_name_cleaned:
                  card_image = "https://lotrtcgwiki.com/wiki/_media/cards:lotr" + splitEditionID(card_id,3) + ".jpg"
                  card_dict = fetchCardDetailsDict("https://lotrtcgwiki.com/wiki/lotr" + splitEditionID(card_id,3))       
                else:
                  card_image = "https://lotrtcgwiki.com/wiki/_media/cards:lotr" + splitEditionID(card_id,2) + ".jpg"
                  card_dict = fetchCardDetailsDict("https://lotrtcgwiki.com/wiki/lotr" + splitEditionID(card_id,2))
                card_dict["card_image"] = card_image
                card_dict["card_name"] = card_name
                card_dict["card_id"] = card_id
                card_dict["set"] = set
                card_dict["card_number"] = card_number
      
                # skipping here as we need to handle promo cards better
                if  "Title" in card_name_cleaned:
                  print("Skipping: " + card_dict.get("card_name",""))
                  i+=1
                  continue
                URL_PRICE = createNewURL(set, card_name_cleaned)
                card_price = getPriceFromURL(URL_PRICE) 
                price_foil = getPriceFromURL(URL_PRICE + "-foil") 
                price_tng  = getPriceFromURL(URL_PRICE + "-tengwar")
                
                if "rarity" not in card_dict.keys():
                  card_dict["rarity"] = "R"
                
                if len(card_dict.get("rarity","")) > 1:
                  card_dict["rarity"] = "P"
                for key, value in card_dict.items():
                  if(key in ["culture","kind","set","card_type","lore","signet"]): 
                    card_dict[key] = value.title()
                                
                if card_dict.get("card_type","") == "Site":
                  card_dict["culture"] = "Site"
                  card_dict["kind"]    = "Site"
                  
                if card_dict.get("card_type","") == "The One Ring":
                  card_dict["culture"] = "The One Ring"
                  card_dict["kind"] = "The One Ring"

                strength_cleaned = None
                vitality_cleaned = None
                if "strength" in card_dict.keys():
                  strength_cleaned = float(card_dict["strength"])
                if "vitality" in card_dict.keys():
                  vitality_cleaned = float(card_dict["vitality"])
                  
                  
                twilight_cleaned = None
                if "twilight" in card_dict.keys():
                  twilight_cleaned = float(card_dict["twilight"])
                
                # Download images from lotrtcgwiki
                #    filename = card_dict.get("card_image","").replace("https://lotrtcgwiki.com/wiki/_media/","")
                #    img_data = requests.get(card_dict.get("card_image","")).content
                #    with open("C:\\Users\\arabo\\Coding\\lotr-tcg-scrapper\\apps\\fe\\src\\res\\images\\"+ filename.replace(":","-"), 'wb') as handler:
                #    handler.write(img_data)
                    
                # log
                # print(json.dumps(str(card_dict),sort_keys=True, indent=4))
    
                # Insert to hasura
                #gql_connector.gqlInsertGenericCard(
                #  "lotr",
                #  card_dict.get("card_id",""),
                #  card_dict.get("card_name",""),
                #  card_dict.get("card_image",""),
                #  editions_dict[card_dict.get("set","")],
                #  card_dict.get("set",""),
                #  card_dict.get("rarity","") + card_dict.get("card_number",""),
                #  rarity_dict[card_dict.get("rarity","")],
                #  float(card_price),
                #  float(price_foil),
                #  float(price_tng),
                #  card_dict.get("card_type",None),
                #  card_dict.get("subtype",None),
                #  card_dict.get("game_text",None),
                #  card_dict.get("lore",None),
                #  twilight_cleaned,
                #  ##### WILL RESULT IN A BUG 100% below line
                #  card_dict.get("site",None),
                #  strength_cleaned,
                #  vitality_cleaned,
                #  card_dict.get("kind",""),
                #)
                print("Inserted" + str(i) + ": " + card_dict.get("card_name",""))
                
                
              ##################### LEGACY SHIT WILL REMOVE AFTER IM DONE WITH ALL FIELDS
               #gql_connector.gqlInsertCard(
               #                        card_dict.get("kind",""),
               #                        card_dict.get("culture",""),
               #                        card_dict.get("resistance",""),
               #                         card_dict.get("home_site",""))
              else:
                  # need to find a way to handle this better
                print("Skipping " + str(i) + ": " + card_dict.get("card_name",""))
                i +=1
                continue
            i += 1

scrapeLatestPricing()
  
print("Process End:", now.strftime("%d/%m/%Y %H:%M:%S"))

