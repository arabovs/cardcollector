import React from "react";

import { Box, Grid, TextField, Typography } from "@mui/material";
import { PricingComponent } from "../components/PricingComponent";

const IndexPage = () => {
  const [inputText, setInputText] = React.useState<any | null>(null);

  return (
    <div>
      {" "}
      <Typography variant="h5" fontWeight={"bold"}>
        All posts:
      </Typography>
      <TextField
        onChange={(e) => {
          if (e.target.value === "") {
            setInputText(null);
            return;
          }
          setInputText(e.target.value.toLowerCase());
        }}
      />
      <PricingComponent inputText={inputText} />
    </div>
  );
};

export default IndexPage;
