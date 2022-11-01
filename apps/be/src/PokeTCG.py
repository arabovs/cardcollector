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
card = Card.find('xy1-1')
gql_connector.gqlInsertGenericCard("pokemon",
                                   card.id,
                                   card.name,
                                   card.images.small,
                                   card.set.id,
                                   card.number,
                                   card.rarity
                                )
