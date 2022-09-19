import React from "react";
import { gql, useSubscription } from "@apollo/client";
import { CardTable } from "../components/CardTable";
import { TopTenFoil } from "../components/TopTenFoil";
import { TopTenTng } from "../components/TopTenTng";
import { Box, Grid, TextField, Typography } from "@mui/material";

import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
  split,
  ApolloProvider,
} from "@apollo/client";

import fetch from "isomorphic-fetch";
import { WebSocketLink } from "@apollo/client/link/ws";
import { getMainDefinition } from "@apollo/client/utilities";
import isNode from "is-node";
import ws from "ws";
import { TopAll } from "../components/TopAll";

const wsLink = new WebSocketLink({
  uri: "wss://lotrtcgwebscrapper.herokuapp.com/v1/graphql",
  options: {
    reconnect: true,
  },
  webSocketImpl: isNode ? ws : null,
});

const httpLink = createHttpLink({
  uri: "https://lotrtcgwebscrapper.herokuapp.com/v1/graphql",
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

const IndexPage = () => {
  const [inputText, setInputText] = React.useState(null);

  return (
    <div>
      {" "}
      <Typography variant="h5" fontWeight={"bold"}>
        All posts:
      </Typography>
      <TextField
        onChange={(e) => {
          if (e.target.value === "") {
            setInputText(null);
            return;
          }
          setInputText(e.target.value.toLowerCase());
        }}
      />
      <CardTable inputText={inputText} />
    </div>
  );
};

export default IndexPage;
