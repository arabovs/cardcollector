import React from "react";
import { gql, useSubscription } from "@apollo/client";
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { client } from "../client/client";

export const SetTable = ({ inputText }) => {
  const { data, loading, error } = useSubscription(
    gql`
      subscription($where: lotr_all_cards_pricing_bool_exp) {
        lotr_all_cards_pricing: lotr_all_cards_pricing(where: $where) {
          card_edition
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
          ? { where: { card_edition: { _ilike: `%${inputText}%` } } }
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
              <TableCell align="left">Set</TableCell>
              <TableCell align="right">Card Name</TableCell>
              <TableCell align="right">Card Price</TableCell>
              <TableCell align="right">Foil Price</TableCell>
              <TableCell align="right">Tang Price</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.lotr_all_cards_pricing.map((row) => (
              <TableRow
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {row.card_edition}
                </TableCell>
                <TableCell align="right">{row.card_name}</TableCell>
                <TableCell align="right">{row.card_price}</TableCell>
                <TableCell align="right">{row.card_price_foil}</TableCell>
                <TableCell align="right">{row.card_price_tng}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};
