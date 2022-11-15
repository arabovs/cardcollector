import React, { createContext, useContext, useState } from "react";
import ThemeTopLayout from "gatsby-theme-material-ui-top-layout/src/components/top-layout";
import { ApolloProvider, useSubscription, gql } from "@apollo/client";
import { client } from "../../client/client";
import {
  AppBar,
  Toolbar,
  Typography,
  MenuItem,
  Select,
  ListItemIcon,
} from "@mui/material";
import { Box } from "@mui/system";
import { Link } from "gatsby-theme-material-ui";
import { TcgIcon } from "../../components/TcgIcon";
import { navigate } from "gatsby";
import { useSelectedGameContext } from "../../../gatsby-browser";

const GameSelector = () => {
  const { data, loading, error } = useSubscription(gql`
    subscription GamesQuery {
      card_details(distinct_on: tcg) {
        tcg
      }
    }
  `);
  const game = useSelectedGameContext();
  if (!game) return null;
  if (loading) return null;
  if (error) return <div>{error.message}</div>;
  return (
    <>
      <Select
        value={game}
        onChange={(e) => navigate(`/${e.target.value}`)}
        size="small"
        sx={{ ml: 2 }}
        renderValue={(selected) => {
          return (
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <ListItemIcon>
                <TcgIcon tcg={selected}></TcgIcon>
              </ListItemIcon>
            </Box>
          );
        }}
      >
        {data.card_details.map(({ tcg }) => (
          <MenuItem value={tcg}>
            <ListItemIcon>
              <TcgIcon tcg={tcg}></TcgIcon>
            </ListItemIcon>
          </MenuItem>
        ))}
      </Select>
    </>
  );
};

export const Navigation = ({ children }) => (
  <>
    <AppBar color="default" position="static" variant="outlined">
      <Toolbar>
        <Link to="/" color="inherit" sx={{ textDecoration: "none" }}>
          <Typography variant="h5">Cardcatalogue</Typography>
        </Link>
        <GameSelector />
      </Toolbar>
    </AppBar>
    {children}
  </>
);

export default function TopLayout({ children, theme }) {
  return (
    <ThemeTopLayout theme={theme}>
      <ApolloProvider client={client}>{children}</ApolloProvider>
    </ThemeTopLayout>
  );
}
