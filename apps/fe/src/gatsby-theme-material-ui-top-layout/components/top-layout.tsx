import React from "react";
import ThemeTopLayout from "gatsby-theme-material-ui-top-layout/src/components/top-layout";
import { ApolloProvider } from "@apollo/client";
import { client } from "../../client/client";
import { AppBar, Toolbar, Typography, IconButton } from "@mui/material";
import { Box } from "@mui/system";
import {
  AccountCircleOutlined,
  ShoppingCartOutlined,
} from "@mui/icons-material";
import { Link } from "gatsby-theme-material-ui";

export default function TopLayout({ children, theme }) {
  return (
    <ThemeTopLayout theme={theme}>
      <ApolloProvider client={client}>
        <AppBar color="default" position="static" variant="outlined">
          <Toolbar>
            <Link to="/" color="inherit" sx={{ textDecoration: "none" }}>
              <Typography variant="h5">Lotrmarket</Typography>
            </Link>
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
      </ApolloProvider>
    </ThemeTopLayout>
  );
}
