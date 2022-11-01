import requests
import sys

# The query !"forest" gets cards named exactly "forest".
url = 'https://api.scryfall.com/cards/search?q=!"thoughtseize"&unique=prints'
forest_info = requests.get(url).json()
for datum in forest_info["data"]:
    print(datum.get("name",""))
    print(datum.get("set_name",""))
    print(datum["image_uris"]["normal"])
    print(datum.get("mana_cost",""))
    print(datum.get("cmc",""))
    print(datum.get("type_line",""))
    print(datum.get("oracle_text",""))
    print(datum.get("power",""))
    print(datum.get("toughness",""))
    print(datum.get("colors",""))
    print(datum.get("color_identity",""))
    print(datum.get("keywords",""))
    print(datum.get("collector_number",""))
    print(datum.get("rarity",""))
    print(datum.get("flavor_text","None"))
    print(datum.get("artist",""))
    print(datum["prices"]["usd"])
    print(datum["prices"]["usd_foil"])
    print(datum["prices"]["usd_etched"])
    print(datum["prices"]["eur"])
    print(datum["prices"]["eur_foil"])
    print(datum["prices"]["tix"])