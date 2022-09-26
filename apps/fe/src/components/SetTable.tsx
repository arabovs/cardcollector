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
          card_img
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
              <TableCell align="left">
                <Typography>Set</Typography>
              </TableCell>
              <TableCell align="right">
                <Typography>Card Name</Typography>
              </TableCell>
              <TableCell align="right">
                <Typography>Card Price</Typography>
              </TableCell>
              <TableCell align="right">
                <Typography>Foil Price</Typography>
              </TableCell>
              <TableCell align="right">
                <Typography>Tang Price</Typography>
              </TableCell>
              <TableCell align="right">
                <Typography>Image</Typography>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.lotr_all_cards_pricing.map((row) => (
              <TableRow
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  <Typography>{row.card_edition}</Typography>
                </TableCell>
                <TableCell align="right">
                  <Typography>{row.card_name}</Typography>
                </TableCell>
                <TableCell align="right">
                  <Typography>{row.card_price}</Typography>
                </TableCell>
                <TableCell align="right">
                  <Typography>{row.card_price_foil}</Typography>
                </TableCell>
                <TableCell align="right">
                  <Typography>{row.card_price_tng}</Typography>
                </TableCell>
                <TableCell align="right">
                  <TableCell align="right">
                    <img src={row.card_img} width="200" height="250" />
                  </TableCell>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};
