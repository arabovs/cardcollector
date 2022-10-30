from http import client
from gql.transport.requests import RequestsHTTPTransport
from requests import request
from gql import Client, gql

class GQL:

    def __init__(self):
        print("Starting DB")

    def gqlInsertCard(self,
                      card_name,
                      card_edition,
                      card_price,
                      card_price_foil,
                      card_price_tng,
                      source, card_id,
                      card_img,card_kind,
                      card_culture,
                      card_twilight,
                      card_type,
                      card_number,
                      lore,
                      card_text,
                      strength,
                      vitality,
                      resistance,
                      rarity,
                      card_signet
                      ):
        HASURA_URL = "https://lotrtcgwebscrapper.herokuapp.com/v1/graphql"

        transport = RequestsHTTPTransport(
            url=HASURA_URL,
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""mutation MyMutation($card_name: String!,
                                           $card_edition: String!,
                                           $card_price: float8!,
                                           $card_price_foil: float8!, 
                                           $card_price_tng: float8!,
                                           $source: String!,
                                           $card_id: String!,
                                           $card_img: String!,
                                           $card_kind: String!,
                                           $card_culture: String!,
                                           $card_twilight: String!,
                                           $card_number: String!,
                                           $card_type: String!,
                                           $lore: String!,
                                           $card_text: String!,
                                           $strength: String!,
                                           $vitality: String!,
                                           $resistance: String!,
                                           $rarity: String!,
                                           $card_signet: String!) {
          insert_lotr_all_cards_pricing(objects: {card_name: $card_name,
                                          card_edition: $card_edition,
                                          card_price: $card_price,
                                          card_price_foil: $card_price_foil, 
                                          card_price_tng: $card_price_tng,
                                          card_id: $card_id,
                                          card_img: $card_img,
                                          card_kind: $card_kind,
                                          card_culture: $card_culture,
                                          card_twilight: $card_twilight,
                                          card_type: $card_type,
                                          card_number: $card_number,
                                          source: $source,
                                          card_lore: $lore,
                                          card_text: $card_text,
                                          strength: $strength,
                                          vitality: $vitality,
                                          resistance: $resistance,
                                          rarity: $rarity,
                                          card_signet: $card_signet
                                          }) {
            affected_rows
          }
        }""")
        params = {
            "card_name": card_name,
            "card_edition": card_edition,
            "card_price": card_price,
            "card_price_foil": card_price_foil,
            "card_price_tng": card_price_tng,
            "card_id": card_id,
            "card_img": card_img,
            "card_kind": card_kind,
            "card_culture": card_culture,
            "card_twilight": card_twilight,
            "card_type": card_type,
            "card_number": card_number,
            "source": source,
            "lore": lore,
            "card_text": card_text,
            "strength": strength,
            "vitality": vitality,
            "resistance": resistance,
            "rarity": rarity,
            "card_signet": card_signet,
            
        }
        result = client.execute(query, variable_values=params)
        return result


    def gqlFindCardbyName(self, card_name):
        query = gql("""query MyQuery($card_name: String!) {
          lotr_all_cards_pricing(where: {card_name: {_ilike: $card_name}}) {
                id
                card_name
                card_price
                card_price_foil
                card_price_tng
          }
        }""")
        params = {
            "card_name": ("%"+card_name+"%"),
        }
        result = client.execute(query, variable_values=params)
        return result
