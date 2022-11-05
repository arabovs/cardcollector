import {
  Card,
  CardMedia,
  CardContent,
  Typography,
  Box,
  Tooltip,
} from "@mui/material";
import { Link } from "gatsby";
import { CardActionArea } from "gatsby-theme-material-ui";
import React from "react";

export const GameCard = ({ id, image, name, set }) => {
  return (
    <Card variant="outlined">
      <CardActionArea component={Link} to={`/card/${id}`}>
        <CardMedia component="img" image={image} />
        <CardContent>
          <Tooltip title={name}>
            <Typography gutterBottom variant="subtitle2" noWrap>
              {name}
            </Typography>
          </Tooltip>
          <Box display="flex" alignItems={"center"}>
            <Tooltip title={set}>
              <Typography variant="body2" color="text.secondary" noWrap>
                {set}
              </Typography>
            </Tooltip>
          </Box>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};
