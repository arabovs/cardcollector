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
      <ImageList sx={{ width: 500, height: 450 }} cols={3} rowHeight={164}>
        <ImageListItem>
          <img src="https://lotrtcgwiki.com/wiki/_media/cards:lotr00001.jpg" />
        </ImageListItem>
      </ImageList>
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
