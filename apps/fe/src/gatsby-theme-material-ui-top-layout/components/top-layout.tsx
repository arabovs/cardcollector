import React from "react";
import ThemeTopLayout from "gatsby-theme-material-ui-top-layout/src/components/top-layout";
import { ApolloProvider } from "@apollo/client";
import { client } from "../../client/client";

export default function TopLayout({ children, theme }) {
  return (
    <ThemeTopLayout theme={theme}>
      <ApolloProvider client={client}>{children}</ApolloProvider>
    </ThemeTopLayout>
  );
}
