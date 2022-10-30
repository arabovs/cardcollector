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
  ListItemText,
  TextField,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import { ExpandLess, ExpandMore, FilterList } from "@mui/icons-material";

const CardFilter = ({
  filters = [],
  filterName,
  selectedFilters,
  setSelectedFilters,
  field,
}) => {
  const [isFilterTypeOpen, setFilterTypeOpen] = useState(false);
  return (
    <>
      <ListItemButton onClick={() => setFilterTypeOpen((p) => !p)}>
        <ListItemText primary={filterName} />
        {isFilterTypeOpen ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Collapse in={isFilterTypeOpen} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          {filters.map((type) => (
            <ListItem
              sx={{ pl: 4 }}
              secondaryAction={
                <Checkbox
                  edge="end"
                  onChange={() => {
                    const currentIndex = selectedFilters.indexOf(type[field]);
                    const newChecked = [...selectedFilters];

                    if (currentIndex === -1) {
                      newChecked.push(type[field]);
                    } else {
                      newChecked.splice(currentIndex, 1);
                    }

                    setSelectedFilters(newChecked);
                  }}
                  checked={selectedFilters.indexOf(type[field]) !== -1}
                />
              }
            >
              <ListItemText primary={type[field]} />
            </ListItem>
          ))}
        </List>
      </Collapse>
    </>
  );
};

const IndexPage = () => {
  const [searchField, setSearchField] = useState("");
  const [isFilterOpen, setFilterOpen] = useState(true);
  const [typeFiterItems, setTypeFilterItems] = useState([]);
  const [kindFilterItems, setKindFilterItems] = useState([]);
  const [cultureFiterItems, setCultureFilterItems] = useState([]);
  const [editionFiterItems, setEditionFilterItems] = useState([]);
  const cardTypeQuery = useQuery(gql`
    query CardTypes {
      lotr_all_cards_pricing(distinct_on: card_type) {
        card_type
      }
    }
  `);
  const cardKindQuery = useQuery(gql`
    query CardTypes {
      lotr_all_cards_pricing(distinct_on: card_kind) {
        card_kind
      }
    }
  `);
  const cardCultureQuery = useQuery(gql`
    query CardTypes {
      lotr_all_cards_pricing(distinct_on: card_culture) {
        card_culture
      }
    }
  `);
  const cardEditionQuery = useQuery(gql`
    query CardTypes {
      lotr_all_cards_pricing(distinct_on: card_edition) {
        card_edition
      }
    }
  `);
  const { data, error } = useSubscription(
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
          ...(kindFilterItems.length > 0
            ? {
                _and: [
                  ...kindFilterItems.map((filter) => ({
                    card_kind: { _eq: filter },
                  })),
                ],
              }
            : {}),
          ...(cultureFiterItems.length > 0
            ? {
                _and: [
                  ...cultureFiterItems.map((filter) => ({
                    card_culture: { _eq: filter },
                  })),
                ],
              }
            : {}),
          ...(editionFiterItems.length > 0
            ? {
                _and: [
                  ...editionFiterItems.map((filter) => ({
                    card_edition: { _eq: filter },
                  })),
                ],
              }
            : {}),
        },
      },
    }
  );
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
          <Grid item sm={2} xs={12}>
            <Card>
              <CardContent>
                <List>
                  <CardFilter
                    filterName="Type"
                    filters={cardTypeQuery.data?.lotr_all_cards_pricing}
                    selectedFilters={typeFiterItems}
                    setSelectedFilters={setTypeFilterItems}
                    field="card_type"
                  />
                  <CardFilter
                    filterName="Kind"
                    filters={cardKindQuery.data?.lotr_all_cards_pricing}
                    selectedFilters={kindFilterItems}
                    setSelectedFilters={setKindFilterItems}
                    field="card_kind"
                  />
                  <CardFilter
                    filterName="Culture"
                    filters={cardCultureQuery.data?.lotr_all_cards_pricing}
                    selectedFilters={cultureFiterItems}
                    setSelectedFilters={setCultureFilterItems}
                    field="card_culture"
                  />
                  <CardFilter
                    filterName="Edition"
                    filters={cardEditionQuery.data?.lotr_all_cards_pricing}
                    selectedFilters={editionFiterItems}
                    setSelectedFilters={setEditionFilterItems}
                    field="card_edition"
                  />
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
          {/* <Grid item sm={12} container spacing={1}>
            {[
              ...typeFiterItems,
              ...kindFilterItems,
              ...cultureFiterItems,
              ...editionFiterItems,
            ].map((typeFilter) => (
              <Grid item>
                <Chip
                  label={`${typeFilter}`}
                  onDelete={() => {
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
          </Grid> */}
          {data?.lotr_all_cards_pricing.map((item) => (
            <Grid item sm={2}>
              <Card>
                <CardMedia component="img" image={item.card_img} />
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
