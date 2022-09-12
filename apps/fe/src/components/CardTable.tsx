import React from "react";
import { gql, useSubscription } from "@apollo/client";
import {
  Chip,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

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

export const CardTable = ({ inputText }) => {
  const { data, loading, error } = useSubscription(
    gql`
      subscription($where: lotr_all_cards_pricing_bool_exp) {
        lotr_all_cards_pricing: lotr_all_cards_pricing(where: $where) {
          card_name
          card_price
          card_price_foil
          card_price_tng
        }
      }
    `,
    {
      client,
      variables: {
        ...(inputText
          ? { where: { card_name: { _ilike: `%${inputText}%` } } }
          : {}),
      },
    }
  );
  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;
  return (
    <div>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Post</TableCell>
              <TableCell align="right">Card Name</TableCell>
              <TableCell align="right">Card Price</TableCell>
              <TableCell align="right">Last Update</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.lotr_all_cards_pricing.map((row) => (
              <TableRow
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {row.card_name}
                </TableCell>
                <TableCell align="right">{row.card_price}</TableCell>
                <TableCell align="right">
                  <div>
                    <Typography variant="caption">
                      {new Date(row.created_at).toLocaleDateString()}{" "}
                      {new Date(row.created_at).toLocaleTimeString()}
                    </Typography>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};
