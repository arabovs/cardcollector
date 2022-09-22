import React from "react";
import { Link } from "gatsby";
import { Box, Grid, TextField, Typography } from "@mui/material";
import { PricingComponent } from "../components/PricingComponent";
import Image from "material-ui-image";
import ImageList from "@mui/material/ImageList";
import ImageListItem from "@mui/material/ImageListItem";

const IndexPage = () => {
  const [inputText, setInputText] = React.useState<any | null>(null);

  return (
    <div>
      {" "}
      <Link to="/search">Go to search</Link>
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
