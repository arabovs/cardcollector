from http import client
from gql.transport.requests import RequestsHTTPTransport
from requests import request
from gql import Client, gql

class GQL:

    def gqlInsertGenericCard(
                            self,
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
                            kind,
                            lotr_resistance,
                            keywords,
                            lotr_culture,
                            lotr_home_site
                          ):
            HASURA_URL = "https://card-catalogue-dev.herokuapp.com/v1/graphql"

            transport = RequestsHTTPTransport(
                url=HASURA_URL,
                verify=True,
                retries=3,
                headers={'x-hasura-admin-secret':'UV7IwHyrnytgUyqT2E5oWixWLxD01gNJ4tDgtCjEqtl2MXPLisCPRWAqsU1FsgXW'},
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
                                               $cost: float8!,
                                               $cost_text: String!,
                                               $attack: float8!,
                                               $defence: float8!,
                                               $kind: String!,
                                               $lotr_resistance: Int!,
                                               $keywords: String!,
                                               $lotr_culture: String!,
                                               $lotr_home_site: String!
                                             ) {
              insert_card_details(objects: {  
                                              tcg: $tcg,
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
                                              kind: $kind,
                                              lotr_resistance: $lotr_resistance,
                                              keywords: $keywords,
                                              lotr_culture: $lotr_culture,
                                              lotr_home_site: $lotr_home_site,
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
                "lotr_resistance": lotr_resistance,
                "keywords": keywords,
                "lotr_culture": lotr_culture,
                "lotr_home_site": lotr_home_site,                      
            }
            result = client.execute(query, variable_values=params)
            return result
    
    
    # BULK INSERT
    def gqlInsertCards(self, objects):
      HASURA_URL = "https://card-catalogue-dev.herokuapp.com/v1/graphql"
      transport = RequestsHTTPTransport(
          url=HASURA_URL,
          verify=True,
          retries=3,
          headers={'x-hasura-admin-secret':'UV7IwHyrnytgUyqT2E5oWixWLxD01gNJ4tDgtCjEqtl2MXPLisCPRWAqsU1FsgXW'},
      )
      client = Client(transport=transport, fetch_schema_from_transport=True)
      query = gql("""mutation MyMutation($objects: [card_details_insert_input!]!) {
            insert_card_details(objects: $objects) {
              affected_rows
            }
          }""")
      variables = {'objects': objects}
      #r = requests.post(url, json={'query': query , 'variables': variables})
      result = client.execute(query, variable_values=variables)
      return result
