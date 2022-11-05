import React, { createContext, useContext, useState } from "react";
import ThemeTopLayout from "gatsby-theme-material-ui-top-layout/src/components/top-layout";
import { ApolloProvider, useSubscription, gql } from "@apollo/client";
import { client } from "../../client/client";
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  MenuItem,
  Select,
} from "@mui/material";
import { Box } from "@mui/system";
import {
  AccountCircleOutlined,
  ShoppingCartOutlined,
} from "@mui/icons-material";
import { Link } from "gatsby-theme-material-ui";
import { TcgIcon } from "../../components/TcgIcon";

const GAME_NAMES = {
  lotr: "The Lord of the Rings",
  mtg: "Magic: The Gathering",
  pokemon: "Pokémon",
  yugioh: "Yu-Gi-Oh!",
  hearthstone: "Heartstone (new)",
};

const GameSelectorContext = createContext(null);

const GameSelectorProvider = ({ children }) => {
  const [selectedGame, setSelectedGame] = useState("lotr");
  return (
    <GameSelectorContext.Provider value={{ selectedGame, setSelectedGame }}>
      {children}
    </GameSelectorContext.Provider>
  );
};
export const useGameSelectorContext = () => {
  const selected = useContext(GameSelectorContext);
  return selected;
};

const GameSelector = () => {
  const { data, loading, error } = useSubscription(gql`
    subscription GamesQuery {
      card_generic(distinct_on: tcg) {
        tcg
      }
    }
  `);
  const { selectedGame, setSelectedGame } = useGameSelectorContext();
  if (loading) return null;
  if (error) return <div>{error.message}</div>;
  return (
    <>
      <Select
        value={selectedGame}
        onChange={(e) => setSelectedGame(e.target.value)}
        size="small"
        sx={{ ml: 2 }}
      >
        {data.card_generic.map(({ tcg }) => (
          <Box display="flex">
            <TcgIcon tcg={tcg}></TcgIcon>
            <MenuItem value={tcg}>{GAME_NAMES[tcg]}</MenuItem>
          </Box>
        ))}
      </Select>
    </>
  );
};

export default function TopLayout({ children, theme }) {
  return (
    <ThemeTopLayout theme={theme}>
      <ApolloProvider client={client}>
        <GameSelectorProvider>
          <AppBar color="default" position="static" variant="outlined">
            <Toolbar>
              <Link to="/" color="inherit" sx={{ textDecoration: "none" }}>
                <Typography variant="h5">Lotrmarket</Typography>
              </Link>
              <GameSelector />
              <Box flex={1} />
              <IconButton>
                <AccountCircleOutlined />
              </IconButton>
              <IconButton>
                <ShoppingCartOutlined />
              </IconButton>
            </Toolbar>
          </AppBar>
          {children}
        </GameSelectorProvider>
      </ApolloProvider>
    </ThemeTopLayout>
  );
}
