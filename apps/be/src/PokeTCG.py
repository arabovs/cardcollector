from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity
from pokemontcgsdk import RestClient
from GQL import GQL
RestClient.configure('f2272cb7-adb2-4e2a-9384-2d64e983fca2')

gql_connector = GQL()
card = Card.where(q='name:Altaria')

def printInsert(option):
    if option ==1:
        print(card[0])
    else:
        gql_connector.gqlInsertGenericCard("pokemon",
                                   card[0].id,
                                   card[0].name,
                                   card[0].images.small,
                                   card[0].set.id,
                                   card[0].number,
                                   card[0].rarity
                                )

printInsert(2)



