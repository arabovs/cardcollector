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
  Typography,
} from "@mui/material";
import { client } from "../client/client";

export const TopTenFoil = ({ inputText }) => {
  const { data, loading, error } = useSubscription(
    gql`
      subscription($where: lotr_all_cards_pricing_bool_exp) {
        lotr_all_cards_pricing: lotr_all_cards_pricing(
          where: $where
          order_by: { card_price_foil: desc }
          limit: 5
        ) {
          card_name
          card_edition
          card_price_foil
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
              <TableCell align="right">Card Name</TableCell>
              <TableCell align="right">Card Edition</TableCell>
              <TableCell align="right">Foil Price</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.lotr_all_cards_pricing.map((row) => (
              <TableRow
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell align="right">{row.card_name}</TableCell>
                <TableCell align="right">{row.card_edition}</TableCell>
                <TableCell align="right">{row.card_price_foil}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};
