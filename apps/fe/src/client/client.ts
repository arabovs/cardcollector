import { ApolloClient, InMemoryCache, HttpLink, split } from "@apollo/client";
import { getMainDefinition } from "@apollo/client/utilities";
import ws from "ws";
import isNode from "is-node";
import { GraphQLWsLink } from "@apollo/client/link/subscriptions";
import { createClient } from "graphql-ws";
import { setContext } from "@apollo/client/link/context";
import fetch from "isomorphic-fetch";

const wsLink = new GraphQLWsLink(
  createClient({
    url: "wss://card-catalogue-dev.herokuapp.com/v1/graphql",
    webSocketImpl: isNode ? ws : null,
    connectionParams: () => {
      return {
        headers: {
          "x-hasura-admin-secret":
            "UV7IwHyrnytgUyqT2E5oWixWLxD01gNJ4tDgtCjEqtl2MXPLisCPRWAqsU1FsgXW",
        },
      };
    },
  })
);

const authLink = setContext((_, { headers }) => {
  return {
    headers: {
      ...headers,
      "x-hasura-admin-secret":
        "UV7IwHyrnytgUyqT2E5oWixWLxD01gNJ4tDgtCjEqtl2MXPLisCPRWAqsU1FsgXW",
    },
    fetch,
  };
});

const httpLink = new HttpLink({
  uri: "https://card-catalogue-dev.herokuapp.com/v1/graphql",
});

const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    );
  },
  wsLink,
  authLink.concat(httpLink)
);

export const client = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache(),
});
