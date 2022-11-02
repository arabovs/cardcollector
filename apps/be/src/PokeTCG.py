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




def insertCard(card):
    def printInsert(option):
        if option == 1:
            print(card)

        else:
            #clean subtype
            subtype_cleaned = ""
            for subtype in card.subtypes:
                subtype_cleaned += "["+subtype+"]"

            #clean flavour text
            if card.flavorText is None:
                card.flavorText = ""
            
            hp_cleaned = None
            if card.hp is None:
                card.hp = None
            else:
                hp_cleaned = float(card.hp)

            #clean rules
            # MAYBE BUG
            card_text_cleaned = ""
            if card.rules is None: ### why not is not None???? doesnt make sense here
                    card_text_cleaned = None
            else:
                for attack in card.attacks:
                    cost_cleaned = ""
                    for cost in attack.cost:
                        cost_cleaned = cost_cleaned + "[" + cost + "]"
                    card_text_cleaned = "[Attack] Name: " + attack.name + "," + " Cost: " + cost_cleaned + "," + "Cost: " + str(attack.convertedEnergyCost) + "," + "Damage: " + attack.damage + ",\n" + "Text: " + attack.text

            card_types_cleaned = re.sub(r"[^a-zA-Z0-9.:;!?,\s+]","é",card.supertype)
            
            
            # RETREAT Cleanup
            card_retreat_cost_cleaned = ""
            if card.convertedRetreatCost is None:
                card_retreat_cost_cleaned = None
            else:
                card_retreat_cost_cleaned = float(card.convertedRetreatCost)
            
            # RETREAT COST Cleanup
            card_retreat_cost_text_cleaned = ""
            if card.retreatCost is None:
                card_retreat_cost_text_cleaned = None
            else:
                for cost in card.retreatCost:
                        card_retreat_cost_text_cleaned = card_retreat_cost_text_cleaned + "[" + cost + "]"                        

            # RARITY Cleanup
            card_rarity_cleaned = None
            if card.rarity is not None:
                card_rarity_cleaned = str(card.rarity).title()
                  
            gql_connector.gqlInsertGenericCard(
                                      "pokemon",
                                       card.id,
                                       card.name,
                                       card.images.small,
                                       card.set.id,
                                       card.set.id,
                                       card.number,
                                       card_rarity_cleaned,
                                       card.cardmarket.prices.averageSellPrice,
                                       card.cardmarket.prices.lowPrice,
                                       card.cardmarket.prices.trendPrice,
                                       card_types_cleaned,
                                       subtype_cleaned,
                                       card_text_cleaned,
                                       card.flavorText,
                                       card_retreat_cost_cleaned,
                                       card_retreat_cost_text_cleaned,
                                       None, # pokemon monsters' attack/s are included in card_text_cleaned. BUG we should find a way
                                       hp_cleaned, 
                                    )
            

    printInsert(2)

def insertCards(cards):
    i = 0
    for card in cards:
            if i < 300 and i >= 0:
                insertCard(card)    
            if i == 300:
                break
            i+=1

#cards = [
#        Card.where(q='name:"Gym Trainer"'),
#    ]

cards = Card.all()
insertCards(cards)