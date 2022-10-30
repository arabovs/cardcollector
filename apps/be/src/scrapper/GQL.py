from http import client
from gql.transport.requests import RequestsHTTPTransport
from requests import request
from gql import Client, gql

class GQL:

    def __init__(self):
        print("Starting DB")

    def gqlInsertCard(self,
                      card_name,
                      set,
                      card_price,
                      price_foil,
                      price_tng,
                      source, card_id,
                      card_img,kind,
                      culture,
                      twilight,
                      type,
                      card_number,
                      lore,
                      text,
                      strength,
                      vitality,
                      resistance,
                      rarity,
                      signet
                      ):
        HASURA_URL = "https://lotrtcgwebscrapper.herokuapp.com/v1/graphql"

        transport = RequestsHTTPTransport(
            url=HASURA_URL,
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""mutation MyMutation($card_name: String!,
                                           $set: String!,
                                           $card_price: float8!,
                                           $price_foil: float8!, 
                                           $price_tng: float8!,
                                           $source: String!,
                                           $card_id: String!,
                                           $card_img: String!,
                                           $kind: String!,
                                           $culture: String!,
                                           $twilight: String!,
                                           $card_number: String!,
                                           $type: String!,
                                           $lore: String!,
                                           $text: String!,
                                           $strength: String!,
                                           $vitality: String!,
                                           $resistance: String!,
                                           $rarity: String!,
                                           $signet: String!) {
          insert_lotr_all_cards_pricing(objects: {card_name: $card_name,
                                          set: $set,
                                          card_price: $card_price,
                                          price_foil: $price_foil, 
                                          price_tng: $price_tng,
                                          card_id: $card_id,
                                          card_img: $card_img,
                                          kind: $kind,
                                          culture: $culture,
                                          twilight: $twilight,
                                          type: $type,
                                          card_number: $card_number,
                                          source: $source,
                                          lore: $lore,
                                          text: $text,
                                          strength: $strength,
                                          vitality: $vitality,
                                          resistance: $resistance,
                                          rarity: $rarity,
                                          signet: $signet
                                          }) {
            affected_rows
          }
        }""")
        params = {
            "card_name": card_name,
            "set": set,
            "card_price": card_price,
            "price_foil": price_foil,
            "price_tng": price_tng,
            "card_id": card_id,
            "card_img": card_img,
            "kind": kind,
            "culture": culture,
            "twilight": twilight,
            "type": type,
            "card_number": card_number,
            "source": source,
            "lore": lore,
            "text": text,
            "strength": strength,
            "vitality": vitality,
            "resistance": resistance,
            "rarity": rarity,
            "signet": signet,
            
        }
        result = client.execute(query, variable_values=params)
        return result


    def gqlFindCardbyName(self, card_name):
        query = gql("""query MyQuery($card_name: String!) {
          lotr_all_cards_pricing(where: {card_name: {_ilike: $card_name}}) {
                id
                card_name
                card_price
                price_foil
                price_tng
          }
        }""")
        params = {
            "card_name": ("%"+card_name+"%"),
        }
        result = client.execute(query, variable_values=params)
        return result
