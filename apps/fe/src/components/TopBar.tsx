import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Tabs,
  Tab,
  Chip,
} from "@mui/material";
import { navigate } from "gatsby";
import { Button } from "gatsby-theme-material-ui";
import React from "react";

export const TopBar = () => {
  const getPath = () => {
    if (location.pathname === "/buy" || location.pathname === "/") {
      return 0;
    }
    if (location.pathname === "/sell") {
      return 1;
    }
    if (location.pathname === "/history") {
      return 2;
    }
    return null;
  };
  return (
    <AppBar position="static" color="default">
      <Toolbar>
        <Typography sx={{ marginRight: 1, flex: 1 }} fontWeight="bold">
          GameSpace
        </Typography>

        <Box flex={2} display={"flex"} justifyContent="center">
          <Tabs value={getPath()} aria-label="basic tabs example">
            <Tab label="buy" onClick={() => navigate("/buy")} />
            <Tab label="sell" onClick={() => navigate("/sell")} />
            <Tab label="history" onClick={() => navigate("/history")} />
          </Tabs>
        </Box>

        <Box
          sx={{
            flex: 1,
            justifyContent: "flex-end",
            display: "flex",
            alignItems: "center",
          }}
        >
          <>
            <Typography sx={{ marginRight: 1 }} fontWeight="bold">
              AAA
            </Typography>
            <Chip label={<Typography color="inherit">XX</Typography>} />
          </>
        </Box>
      </Toolbar>
    </AppBar>
  );
};
