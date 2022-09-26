from http import client
from gql.transport.requests import RequestsHTTPTransport
from requests import request
from gql import Client, gql

class GQL:

    def __init__(self):
        print("Starting DB")

    def gqlInsertCard(self, card_name, card_edition, card_price, card_price_foil, card_price_tng, source, card_id, card_img):
        HASURA_URL = "https://lotrtcgwebscrapper.herokuapp.com/v1/graphql"

        transport = RequestsHTTPTransport(
            url=HASURA_URL,
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""mutation MyMutation($card_name: String!, $card_edition: String!, $card_price: float8!, $card_price_foil: float8!, $card_price_tng: float8!, $source: String!, $card_id: String!, $card_img: String!) {
          insert_lotr_all_cards_pricing(objects: {card_name: $card_name,
                                          card_edition: $card_edition,
                                          card_price: $card_price,
                                          card_price_foil: $card_price_foil, 
                                          card_price_tng: $card_price_tng,
                                          card_id: $card_id,
                                          card_img: $card_img,
                                          source: $source 
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
            "source": source
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
