from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity
from pokemontcgsdk import RestClient
from GQL import GQL
import re
RestClient.configure('f2272cb7-adb2-4e2a-9384-2d64e983fca2')
gql_connector = GQL()
cards = [
        Card.where(q='name:"Spell Tag"'),
        #Card.where(q='name:"Charizard"'),
        #Card.where(q='name:"Charmander"'),
        #Card.where(q='name:"Abra"'),
        #Card.where(q='name:"Alakazam"'),
        #Card.where(q='name:"Pikachu"'),
        #Card.where(q='name:"Gym Trainer"'),
    ]


def cardSearch(card):
    def printInsert(option):
        if option ==1:
            print(card[0])

        else:
            #clean subtype
            subtype_cleaned = ""
            for subtype in card[0].subtypes:
                subtype_cleaned += "["+subtype+"]"

            #clean flavour text
            if card[0].flavorText is None:
                card[0].flavorText = ""

            #clean rules
            card_text_cleaned = ""
            if card[0].rules is None:
                for attack in card[0].attacks:
                    cost_cleaned = ""
                    for cost in attack.cost:
                        cost_cleaned = cost_cleaned + "[" + cost + "]"
                    card_text_cleaned = "[Attack] Name: " + attack.name + "," + " Cost: " + cost_cleaned + "," + "Cost: " + str(attack.convertedEnergyCost) + "," + "Damage: " + attack.damage + ",\n" + "Text: " + attack.text
            else:
                for rule in card[0].rules:
                    card_text_cleaned = card_text_cleaned + "\n" + rule

            card_types_cleaned = re.sub(r"[^a-zA-Z0-9.:;!?,\s+]","é",card[0].supertype)
            
            gql_connector.gqlInsertGenericCard(
                                      "pokemon",
                                       card[0].id,
                                       card[0].name,
                                       card[0].images.small,
                                       card[0].set.id,
                                       card[0].set.id,
                                       card[0].number,
                                       card[0].rarity.title(),
                                       card[0].cardmarket.prices.averageSellPrice,
                                       card[0].cardmarket.prices.lowPrice,
                                       card[0].cardmarket.prices.trendPrice,
                                       card_types_cleaned,
                                       subtype_cleaned,
                                       card_text_cleaned,
                                       card[0].flavorText,
                                    )

    printInsert(1)



for card in cards:
    cardSearch(card)