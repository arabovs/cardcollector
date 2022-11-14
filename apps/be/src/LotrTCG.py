from operator import concat
from urllib import response
from requests import request
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from etc.postgre.GQL import GQL
from etc.lotrtcg.metadata import HsMetadata
import re
from os.path  import basename
from datetime import datetime

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
       x = 0
     value = str(card_detail_row.find('td', class_='col1')).replace("<td class=\"col1\"> ","").replace("</td>","")
     
     if (str(key) not in  ['game_text','lore','card_type']):
        dict[str(key).lower().replace(" ","_")] = re.sub(r"[^a-zA-Z0-9.:;!?,\s+]","",str(value).replace("<em>","").replace("�","").replace("</em>",""))
     
  return dict

print(str(datetime.now()) + " Process Start")

def getCardEdition(card_id):
  edition = None
  card_id_regex_number = re.compile(r"^([^a-zA-Z]*)\w+(\d+)") 
  card_id_regex_plus = re.compile(r"(\d+)\w+\+\d+") 
  if "+" in card_id:
    edition = re.search(card_id_regex_plus,card_id).group(1)
  elif card_id[-1].isnumeric():
    edition = re.search(card_id_regex_number, card_id).group(1)
  elif card_id[-1] == 'T': 
    edition = "T"
  elif card_id[-3] == 'AFD':
    edition = "0"
  
  return str(edition)

def getCardNumber(card_id):
  card_number = 0
  card_id_regex_number = re.compile(r"^([^a-zA-Z]*)\w+(\d+)") 
  card_number_regex_afd = re.compile(r"^\d+\w+(\d+)T")
  card_number_regex_plus = re.compile(r"\d+\w+\+(\d+)")
  if "+" in card_id:
    card_number = re.search(card_number_regex_plus, card_id).group(1)
  elif card_id[-1].isnumeric():
    card_number = re.search(card_id_regex_number, card_id).group(2)
  elif card_id[-3] == 'AFD':
    card_number = 1
  elif card_id[-1] == 'T':
    card_number = re.search(card_number_regex_afd, card_id).group(1)
      
  return str(card_number)

def scrapeLatestPricing():
    cards_table = soup.find_all('table', class_='inline')
    i = 0
    for cards in cards_table:
        rows = cards.find_all('tr')
        for row in rows:
            if i > 0:
              # Basic Card info from Grand Page
              card_id = str(row.find('td').string)
              card_name = str(row.find('td', class_= 'col1').string)
              card_url = str(row.find('td', class_= 'col1').a.get("href"))

              card_name_cleaned = cleanCardName(card_name) 
              
              card_name_cleaned.replace("+","")
              card_dict = fetchCardDetailsDict("https://lotrtcgwiki.com" + card_url)
              card_dict["card_name"] = card_name.replace(" (AI)","").replace(" (M)","").replace(" (T)","").replace(" (P)","").replace(" (AFD)","").replace(" (D)","").replace(" (AFD)","").replace(" (SPD)","").replace(" (W)","").replace(" (F)","").replace(" (F)","").replace(" (O)","")
              card_dict["card_id"] = card_id
              card_dict["card_image"] = "https://lotrtcgwiki.com/wiki/_media/cards:" + card_url.replace("/wiki/","") + ".jpg"
              card_dict["set"] = getCardEdition(card_id)
              card_dict["card_number"] = getCardNumber(card_id)
    
              # skipping here as we need to handle promo cards better
              if  "Title" in card_name_cleaned:
                print("Skipping: " + card_dict.get("card_name",""))
                i+=1
                continue
              #URL_PRICE = createNewURL(set, card_name_cleaned)
              #card_price = getPriceFromURL(URL_PRICE) 
              #price_foil = getPriceFromURL(URL_PRICE + "-foil") 
              #price_tng  = getPriceFromURL(URL_PRICE + "-tengwar")
              
              # Site's culture and kind
              if card_dict["card_type"] == " Site":
                card_dict["culture"] = "Site"
                card_dict["kind"] = "Site"
              
              # The One Ring's culture and kind
              if card_dict["card_type"] == " The One Ring":
                card_dict["culture"] = "The One Ring"
                card_dict["kind"] = "The One Ring"
              
              # clean ups
              strength_cleaned = None
              if "strength" in card_dict.keys():
                strength_cleaned = float(card_dict["strength"])
                
              vitality_cleaned = None
              if "vitality" in card_dict.keys():
                vitality_cleaned = float(card_dict["vitality"])
                
              resistance_cleaned = None
              if "resistance" in card_dict.keys():
                resistance_cleaned = int(card_dict["resistance"])
                
              twilight_cleaned = None
              if "twilight" in card_dict.keys():
                twilight_cleaned = float(card_dict["twilight"])
                
              if "rarity" not in card_dict.keys():
                card_dict["rarity"] = "R"
              
              if len(card_dict.get("rarity","")) > 1:
                card_dict["rarity"] = "P"
              
              for key, value in card_dict.items():
                if(key in ["culture","kind","set","card_type","lore","signet"]): 
                  card_dict[key] = value.title()
                
              # Download images from lotrtcgwiki
              #    filename = card_dict.get("card_image","").replace("https://lotrtcgwiki.com/wiki/_media/","")
              #    img_data = requests.get(card_dict.get("card_image","")).content
              #    with open("C:\\Users\\arabo\\Coding\\lotr-tcg-scrapper\\apps\\fe\\src\\res\\images\\"+ filename.replace(":","-"), 'wb') as handler:
              #    handler.write(img_data)
                  
              # log
              # print(json.dumps(str(card_dict),sort_keys=True, indent=4))
  
              # Insert to hasura
              gql_connector.gqlInsertGenericCard(
                "lotr",												                          			# card_details.tcg		
                card_dict.get("card_id",""),                                  # card_details.api_id
                card_dict.get("card_name",""),                                # card_details.name
                card_dict.get("card_image",""),                               # card_details.image
                editions_dict[card_dict.get("set","")],                       # card_details.set
                card_dict.get("set","s"),                                     # card_details.set_id
                card_dict.get("rarity","") + card_dict.get("card_number",""), # card_details.card_id
                rarity_dict[card_dict.get("rarity","")],                      # card_details.rarity
                0, #float(card_price),                                        # card_details.price
                0, #float(price_foil),                                        # card_details.price_foil
                0, #float(price_tng),                                         # card_details.price_other
                card_dict.get("card_type",None),                              # card_details.type
                card_dict.get("subtype",None),                                # card_details.subtype
                card_dict.get("game_text",None),                              # card_details.game_text
                card_dict.get("lore",None),                                   # card_details.flavor_text
                twilight_cleaned,                                             # card_details.cost
                card_dict.get("site",None),                                   # card_details.cost_text
                strength_cleaned,                                             # card_details.attack
                vitality_cleaned,                                             # card_details.defence
                card_dict.get("kind",None),                                   # card_details.kind       
                resistance_cleaned,                                           # card_details.lotr_resistance
                None,                                                         # card_details.keywords (FEATURE)
                card_dict.get("culture",None),                                # card_details.lotr_culture   
                card_dict.get("home_site",None),                              # card_details.lotr_home_site
                None,
                None
                    
              )
              print(str(datetime.now()) + " Inserted " + str(i) + ": " + card_dict.get("card_name",""))
            i += 1

scrapeLatestPricing()
  
print(str(datetime.now()) +" Process End")

