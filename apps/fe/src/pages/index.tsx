import React from "react";
import { gql, useSubscription } from "@apollo/client";
import { client } from "../client/client";
import {
  Chip,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

const IndexPage = () => {
  const { data, loading, error } = useSubscription(
    gql`
      subscription {
        lotr_all_cards_pricing: lotr_all_cards_pricing(
          order_by: { card_price: desc }
          limit: 10
        ) {
          card_name
          card_price
          created_at
        }
      }
    `
  );
  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;

  return (
    <div>
      {" "}
      <Typography variant="h5" fontWeight={"bold"}>
        All posts:
      </Typography>
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

export default IndexPage;
