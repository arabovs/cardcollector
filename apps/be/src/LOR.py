import requests
import json
import time
from datetime import datetime

from etc.postgre.GQL import GQL
from etc.hearthstone.metadata import metadata
from etc.helpers.helper import helper

TCG = "lor"


data= {
    "associatedCards": [],
    "associatedCardRefs": [],
    "assets": [
      {
        "gameAbsolutePath": "http://dd.b.pvp.net/3_19_0/set1/en_us/img/cards/01IO012.png",
        "fullAbsolutePath": "http://dd.b.pvp.net/3_19_0/set1/en_us/img/cards/01IO012-full.png"
      }
    ],
    "regions": ["Ionia"],
    "regionRefs": ["Ionia"],
    "attack": 0,
    "cost": 2,
    "health": 0,
    "description": "Give an ally +2|+0 or +0|+3 this round.",
    "descriptionRaw": "Give an ally +2|+0 or +0|+3 this round.",
    "levelupDescription": "",
    "levelupDescriptionRaw": "",
    "flavorText": "\"Never fear change. It will question you, test your limits. It is our greatest teacher.\" - Karma",
    "artistName": "SIXMOREVODKA",
    "name": "Twin Disciplines",
    "cardCode": "01IO012",
    "keywords": ["Burst"],
    "keywordRefs": ["Burst"],
    "spellSpeed": "Burst",
    "spellSpeedRef": "Burst",
    "rarity": "COMMON",
    "rarityRef": "Common",
    "subtypes": [],
    "supertype": "",
    "type": "Spell",
    "collectible": 1,
    "set": "Set1"
}

regions_cleaned = ""
if len(data["regions"]) > 0 :
    for region in data["regions"]:
        regions_cleaned == regions_cleaned +"|" + region
else:
    regions_cleaned = None


   


subtypes_cleaned = ""
if len(data["subtypes"]) > 0 :
    for subtype in data["subtypes"]:
        subtypes_cleaned == subtypes_cleaned + "|" + subtype
else:
    subtypes_cleaned=None


gql_connector = GQL()


gql_connector.gqlInsertCards(helper.returnObject(
    TCG,
    data["cardCode"],
    data["name"],
    data["assets"][0]["gameAbsolutePath"],
    data["set"], #need name
    data["set"],
    data["cardCode"],
    data["rarity"],
    0,
    0,
    0,
    data["type"],
    subtypes_cleaned,
    data["description"],
    data["flavorText"],
    data["cost"],
    str(data["cost"]),
    data["attack"],
    data["health"],
    regions_cleaned
    



))



