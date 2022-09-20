import React from "react";
import { Box, Grid } from "Grommet";
import { SetTable } from "./SetTable";

export const SetComponent = ({ inputText }) => {
  return (
    <div>
      <Grid
        areas={[
          { name: "main", start: [0, 0], end: [1, 0] },
          { name: "side", start: [2, 0], end: [2, 0] },
          
        ]}
        columns={["small", "flex", "medium"]}
        rows={["medium", "small"]}
        gap="small"
      >
        <Box gridArea="main">
          <SetTable inputText={inputText} />
        </Box>
        <Box gridArea="side" />
        <Box gridArea="foot" background="accent-1" />
      </Grid>
    </div>
  );
};
