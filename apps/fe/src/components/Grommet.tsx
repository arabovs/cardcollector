import React from "react";
import { Box, Grid } from "grommet";
import { CardTable } from "../components/CardTable";
import { TopTenFoil } from "../components/TopTenFoil";
import { TopTenTng } from "../components/TopTenTng";

export const Grommet = ({ inputText }) => {
  return (
    <div>
      <Grid
        areas={[
          { name: "nav", start: [0, 0], end: [0, 0] },
          { name: "main", start: [1, 0], end: [1, 0] },
          { name: "side", start: [2, 0], end: [2, 0] },
          { name: "foot", start: [0, 1], end: [2, 1] },
        ]}
        columns={["small", "flex", "medium"]}
        rows={["medium", "small"]}
        gap="small"
      >
        <Box gridArea="nav" background="brand">
          <CardTable inputText={inputText} />
        </Box>
        <Box gridArea="main" background="brand">
          <TopTenTng inputText={inputText} />
        </Box>
        <Box gridArea="side" background="brand" />
        <Box gridArea="foot" background="accent-1" />
      </Grid>
    </div>
  );
};
