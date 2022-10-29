import { useSubscription, gql, useQuery } from "@apollo/client";
import {
  Box,
  Button,
  Card,
  CardContent,
  CardMedia,
  Checkbox,
  Chip,
  Collapse,
  Grid,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  TextField,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import {
  ExpandLess,
  ExpandMore,
  FilterList,
  Inbox,
  StarBorder,
} from "@mui/icons-material";

const IndexPage = () => {
  const [searchField, setSearchField] = useState("");
  const [isFilterOpen, setFilterOpen] = useState(true);
  const [isFilterTypeOpen, setFilterTypeOpen] = useState(false);
  const [typeFiterItems, setTypeFilterItems] = useState([]);
  const cardTypeQuery = useQuery(gql`
    query CardTypes {
      lotr_all_cards_pricing(distinct_on: card_type) {
        card_type
      }
    }
  `);
  const { data, error, ...rest } = useSubscription(
    gql`
      subscription ($where: lotr_all_cards_pricing_bool_exp) {
        lotr_all_cards_pricing: lotr_all_cards_pricing(where: $where) {
          id
          card_name
          card_price
          card_price_foil
          card_price_tng
          card_img
        }
      }
    `,
    {
      variables: {
        where: {
          card_name: { _ilike: `%${searchField}%` },
          ...(typeFiterItems.length > 0
            ? {
                _or: [
                  ...typeFiterItems.map((filter) => ({
                    card_type: { _eq: filter },
                  })),
                ],
              }
            : {}),
        },
      },
    }
  );
  console.log(rest);
  if (error) return <div>{error.message}</div>;
  return (
    <Box sx={{ p: 1 }}>
      <Box display="flex" sx={{ mb: 1, mt: 1 }}>
        <IconButton sx={{ mr: 1 }} onClick={() => setFilterOpen((p) => !p)}>
          <FilterList />
        </IconButton>
        <TextField
          type="text"
          size="small"
          name="search_field"
          fullWidth
          placeholder="Search by name"
          value={searchField}
          onChange={(e) => setSearchField(e.target.value)}
          autoComplete={"off"}
        />
      </Box>
      <Grid container spacing={1}>
        {isFilterOpen && (
          <Grid item sm={2}>
            <Card>
              <CardContent>
                <List>
                  <ListItemButton onClick={() => setFilterTypeOpen((p) => !p)}>
                    <ListItemIcon>
                      <Inbox />
                    </ListItemIcon>
                    <ListItemText primary="Type" />
                    {isFilterTypeOpen ? <ExpandLess /> : <ExpandMore />}
                  </ListItemButton>
                  <Collapse in={isFilterTypeOpen} timeout="auto" unmountOnExit>
                    <List component="div" disablePadding>
                      {cardTypeQuery.data?.lotr_all_cards_pricing.map(
                        (type) => (
                          <ListItem
                            sx={{ pl: 4 }}
                            secondaryAction={
                              <Checkbox
                                edge="end"
                                onChange={() => {
                                  const currentIndex = typeFiterItems.indexOf(
                                    type.card_type
                                  );
                                  const newChecked = [...typeFiterItems];

                                  if (currentIndex === -1) {
                                    newChecked.push(type.card_type);
                                  } else {
                                    newChecked.splice(currentIndex, 1);
                                  }

                                  setTypeFilterItems(newChecked);
                                }}
                                checked={
                                  typeFiterItems.indexOf(type.card_type) !== -1
                                }
                              />
                            }
                          >
                            <ListItemIcon>
                              <StarBorder />
                            </ListItemIcon>
                            <ListItemText primary={type.card_type} />
                          </ListItem>
                        )
                      )}
                    </List>
                  </Collapse>
                </List>
              </CardContent>
            </Card>
          </Grid>
        )}

        <Grid container spacing={1} item sm={isFilterOpen ? 10 : 12}>
          <Grid item sm={12}>
            {data?.lotr_all_cards_pricing && (
              <Typography variant="subtitle2">
                {data?.lotr_all_cards_pricing.length} items
              </Typography>
            )}
          </Grid>
          <Grid item sm={12} container spacing={1}>
            {typeFiterItems.map((typeFilter) => (
              <Grid item>
                <Chip
                  label={`Type: ${typeFilter}`}
                  onDelete={() => {
                    console.log("delete");
                    setTypeFilterItems(
                      typeFiterItems.filter((i) => i !== typeFilter)
                    );
                  }}
                />
              </Grid>
            ))}
            {typeFiterItems.length > 0 && (
              <Grid item>
                <Button
                  size="small"
                  color="inherit"
                  onClick={() => setTypeFilterItems([])}
                >
                  Clear all
                </Button>
              </Grid>
            )}
          </Grid>
          {data?.lotr_all_cards_pricing.map((item) => (
            <Grid item sm={2}>
              <Card>
                <CardMedia component="img" height="300" image={item.card_img} />
                <CardContent>
                  <Typography gutterBottom variant="subtitle2" noWrap>
                    {item.card_name}
                  </Typography>
                  <Box display="flex" alignItems={"center"}>
                    <Typography variant="body2" color="text.secondary">
                      {new Intl.NumberFormat("en-US", {
                        style: "currency",
                        currency: "USD",
                      }).format(item.card_price)}
                    </Typography>
                    <Box flex={1} />
                    <Button variant="contained" size="small">
                      buy now
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Grid>
    </Box>
  );
};

export default IndexPage;
