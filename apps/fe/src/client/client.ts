import React from "react";
import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
  split,
} from "@apollo/client";

import fetch from "isomorphic-fetch";
import { WebSocketLink } from "@apollo/client/link/ws";
import { getMainDefinition } from "@apollo/client/utilities";
import isNode from "is-node";
import ws from "ws";

const wsLink = new WebSocketLink({
  uri: "wss://card-catalogue-dev.herokuapp.com/v1/graphql",
  options: {
    reconnect: true,
  },
  webSocketImpl: isNode ? ws : null,
});

const httpLink = createHttpLink({
  uri: "https://card-catalogue-dev.herokuapp.com/v1/graphql",
  fetch,
});

const link = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    );
  },
  wsLink,
  httpLink
);

export const client = new ApolloClient({
  link: link,
  cache: new InMemoryCache(),
});
