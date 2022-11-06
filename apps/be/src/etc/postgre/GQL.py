from http import client
from gql.transport.requests import RequestsHTTPTransport
from requests import request
from gql import Client, gql

class GQL:

    def gqlInsertGenericCard(self,
                            tcg,
                            api_id,
                            name,
                            image,
                            set,
                            set_code,
                            card_id,
                            rarity,
                            price,
                            price_foil,
                            price_other,
                            type,
                            subtype,
                            game_text,
                            flavor_text,
                            cost,
                            cost_text,
                            attack,
                            defence,
                            kind
                          ):
            HASURA_URL = "https://lotrtcgwebscrapper.herokuapp.com/v1/graphql"

            transport = RequestsHTTPTransport(
                url=HASURA_URL,
                verify=True,
                retries=3,
            )
            client = Client(transport=transport, fetch_schema_from_transport=True)
            query = gql("""mutation MyMutation($tcg: String!,
                                               $api_id: String!,
                                               $name: String!,
                                               $image: String!, 
                                               $set: String!,
                                               $set_code: String!,
                                               $card_id: String!,
                                               $rarity: String!,
                                               $price: float8!,
                                               $price_foil: float8!,
                                               $price_other: float8!,
                                               $type: String!,
                                               $subtype: String!,
                                               $game_text: String!,
                                               $flavor_text: String!,
                                               $cost: Int!,
                                               $cost_text: String!,
                                               $attack: float8!,
                                               $defence: float8!,
                                               $kind: String!,
                                             ) {
              insert_card_generic(objects: {tcg: $tcg,
                                              api_id: $api_id,
                                              name: $name, 
                                              image: $image,
                                              set: $set,
                                              set_code: $set_code
                                              card_id: $card_id,
                                              rarity: $rarity,
                                              price: $price,
                                              price_foil: $price_foil,
                                              price_other: $price_other
                                              type: $type,
                                              subtype: $subtype,
                                              game_text: $game_text,
                                              flavor_text: $flavor_text,
                                              cost: $cost,
                                              cost_text: $cost_text,
                                              attack: $attack,
                                              defence: $defence,
                                              kind: $kind
                                              }) {
                affected_rows
              }
            }""")
            params = {
                "tcg": tcg,
                "api_id": api_id,
                "name": name,
                "image": image,
                "set": set,
                "card_id": card_id,
                "set_code": set_code,
                "rarity": rarity,
                "price": price,
                "price_foil": price_foil,
                "price_other": price_other,
                "type": type,
                "subtype": subtype,
                "game_text": game_text,
                "flavor_text": flavor_text,  
                "cost": cost,
                "cost_text": cost_text,
                "attack": attack,
                "defence": defence,
                "kind": kind,          
            }
            result = client.execute(query, variable_values=params)
            return result
    
    
    # BULK INSERT
    def gqlInsertCards(self, objects):
      HASURA_URL = "https://lotrtcgwebscrapper.herokuapp.com/v1/graphql"
      transport = RequestsHTTPTransport(
          url=HASURA_URL,
          verify=True,
          retries=3,
      )
      client = Client(transport=transport, fetch_schema_from_transport=True)
      query = gql("""mutation MyMutation($objects: [card_generic_insert_input!]!) {
            insert_card_generic(objects: $objects) {
              affected_rows
            }
          }""")
      variables = {'objects': objects}
      #r = requests.post(url, json={'query': query , 'variables': variables})
      result = client.execute(query, variable_values=variables)
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
