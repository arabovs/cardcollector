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
  InputAdornment,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  MenuItem,
  Select,
  TextField,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import {
  Close,
  ExpandLess,
  ExpandMore,
  FilterList,
  TypeSpecimen,
} from "@mui/icons-material";

const CardFilter = ({
  filters = [],
  filterName,
  selectedFilters,
  setSelectedFilters,
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
                    const includes = selectedFilters
                      .map((filter) => filter.value)
                      .includes(type.value);
                    if (includes) {
                      return setSelectedFilters(
                        selectedFilters.filter((i) => i.value !== type.value)
                      );
                    }
                    setSelectedFilters([...selectedFilters, type]);
                  }}
                  checked={selectedFilters
                    .map((filter) => filter.value)
                    .includes(type.value)}
                />
              }
            >
              <ListItemText primary={type.value} />
            </ListItem>
          ))}
        </List>
      </Collapse>
    </>
  );
};

const labels = {
  card_type: "Type",
  card_kind: "Kind",
  card_culture: "Culture",
  card_edition: "Edition",
  rarity: "Rarity",
};

const IndexPage = () => {
  const [searchField, setSearchField] = useState("");
  const [isFilterOpen, setFilterOpen] = useState(true);
  const [selectedFilters, setSelectedFilters] = useState([]);
  const [orderBy, setOrderBy] = useState(null);
  const filterTypesQuery = useQuery(gql`
    query FilterTypes {
      card_type: lotr_all_cards_pricing(distinct_on: card_type) {
        card_type
      }
      card_kind: lotr_all_cards_pricing(distinct_on: card_kind) {
        card_kind
      }
      card_culture: lotr_all_cards_pricing(distinct_on: card_culture) {
        card_culture
      }
      card_edition: lotr_all_cards_pricing(distinct_on: card_edition) {
        card_edition
      }
      rarity: lotr_all_cards_pricing(distinct_on: rarity) {
        rarity
      }
    }
  `);
  const filterTypes = (
    (filterTypesQuery.data && Object.entries(filterTypesQuery.data)) ||
    []
  ).map(([key, value]) => ({
    key,
    label: labels[key],
    values: value.map((item) => ({
      key,
      value: item[key],
      label: labels[key],
    })),
  }));
  const { data, error } = useSubscription(
    gql`
      subscription (
        $where: lotr_all_cards_pricing_bool_exp
        $order_by: [lotr_all_cards_pricing_order_by!]
      ) {
        lotr_all_cards_pricing: lotr_all_cards_pricing(
          where: $where
          order_by: $order_by
        ) {
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
          _or: {
            ...selectedFilters.reduce((acc, filter) => {
              return {
                ...acc,
                [filter.key]: {
                  _in: [...(acc[filter.key]?._in || []), filter.value],
                },
              };
            }, {}),
          },
        },
        order_by: { card_price: orderBy },
      },
    }
  );
  if (error) return <div>{error.message}</div>;
  return (
    <Box sx={{ p: 1 }}>
      <Grid container spacing={1}>
        <Grid item sm={10} sx={{ display: "flex", alignItems: "center" }}>
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
        </Grid>
        <Grid item sm={2}>
          <Select
            fullWidth
            size="small"
            value={orderBy}
            onChange={(e) => setOrderBy(e.target.value)}
            endAdornment={
              orderBy && (
                <InputAdornment position="end" sx={{ mr: 3 }}>
                  <IconButton size="small" onClick={() => setOrderBy(null)}>
                    <Close fontSize={"small"} />
                  </IconButton>
                </InputAdornment>
              )
            }
          >
            <MenuItem value={"asc"}>Price low to high</MenuItem>
            <MenuItem value={"desc"}>Price high to low</MenuItem>
          </Select>
        </Grid>
      </Grid>
      <Grid container spacing={1}>
        {isFilterOpen && (
          <Grid item sm={2} xs={12}>
            <Card>
              <CardContent>
                <List>
                  {filterTypes.map((filterType) => (
                    <CardFilter
                      filterName={filterType.label}
                      filters={filterType.values}
                      selectedFilters={selectedFilters}
                      setSelectedFilters={setSelectedFilters}
                    />
                  ))}
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
            {selectedFilters.map((typeFilter) => (
              <Grid item>
                <Chip
                  label={`${typeFilter.label}: ${typeFilter.value}`}
                  onDelete={() => {
                    setSelectedFilters(
                      selectedFilters.filter(
                        (i) => i.value !== typeFilter.value
                      )
                    );
                  }}
                />
              </Grid>
            ))}
            {selectedFilters.length > 0 && (
              <Grid item>
                <Button
                  size="small"
                  color="inherit"
                  onClick={() => {
                    setSelectedFilters([]);
                  }}
                >
                  Clear all
                </Button>
              </Grid>
            )}
          </Grid>
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
