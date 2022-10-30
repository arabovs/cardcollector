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
  ListItemIcon,
  ListItemText,
  MenuItem,
  Pagination,
  Select,
  Skeleton,
  TextField,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import { Close, ExpandLess, ExpandMore, FilterList } from "@mui/icons-material";

const filter_icons = {
  card_culture: {
    Dwarven: "https://lotrtcgwiki.com/wiki/_media/dwarven.gif",
    Gandalf: "https://lotrtcgwiki.com/wiki/_media/gandalf.gif",
    Elven: "https://lotrtcgwiki.com/wiki/_media/elven.gif",
    Gollum: "https://lotrtcgwiki.com/wiki/_media/gollum.gif",
    Gondor: "https://lotrtcgwiki.com/wiki/_media/gondor.gif",
    Rohan: "https://lotrtcgwiki.com/wiki/_media/rohan.gif",
    Shire: "https://lotrtcgwiki.com/wiki/_media/shire.gif",
    Dunland: "https://lotrtcgwiki.com/wiki/_media/dunland.gif",
    Isengard: "https://lotrtcgwiki.com/wiki/_media/isengard.gif",
    Moria: "https://lotrtcgwiki.com/wiki/_media/moria.gif",
    Raider: "https://lotrtcgwiki.com/wiki/_media/raider.gif",
    Sauron: "https://lotrtcgwiki.com/wiki/_media/sauron.gif",
    Wraith: "https://lotrtcgwiki.com/wiki/_media/wraith.gif",
  },
};

const filter_type_label = {
  card_edition: {
    "0": "Promotional",
    "1": "The Fellowship of the Ring",
    "2": "Mines of Moria",
    "3": "Realms of the Elf-lords",
    "4": "The Two Towers",
    "5": "Battle of Helm's Deep",
    "6": "Ents of Fangorn",
    "7": "The Return of the King",
    "8": "Siege of Gondor",
    "9": "Reflections",
    "10": "Mount Doom",
    "11": "Shadows",
    "12": "Black Rider",
    "13": "Bloodlines",
    "14": "Expanded Middle-earth",
    "15": "Hunters",
    "16": "The Wraith Collection",
    "17": "Rise of Saruman",
    "18": "Treachery & Deceit",
  },
  rarity: {
    C: "Common",
    U: "Uncommon",
    R: "Rare",
    P: "Promo",
  },
};

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
              {filter_icons[type.key] && (
                <ListItemIcon>
                  <img src={filter_icons[type.key][type.value]} />
                </ListItemIcon>
              )}
              <ListItemText
                primary={
                  (filter_type_label[type.key] &&
                    filter_type_label[type.key][type.value]) ||
                  type.value
                }
              />
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
  card_signet: "Signet",
};

const IndexPage = () => {
  const [searchField, setSearchField] = useState("");
  const [isFilterOpen, setFilterOpen] = useState(true);
  const [selectedFilters, setSelectedFilters] = useState([]);
  const [orderBy, setOrderBy] = useState(null);
  const [limitItems, setLimitItems] = useState(50);
  const [page, setPage] = React.useState(1);
  const handlePageChange = (event, value: number) => {
    setPage(value);
  };
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
      card_signet: lotr_all_cards_pricing(
        distinct_on: card_signet
        where: { card_signet: { _neq: "" } }
      ) {
        card_signet
      }
    }
  `);
  const queryFilters = selectedFilters.reduce((acc, filter) => {
    return {
      ...acc,
      [filter.key]: {
        _in: [...(acc[filter.key]?._in || []), filter.value],
      },
    };
  }, {});
  const paginationCountQuery = useQuery(
    gql`
      query PaginationCount($where: lotr_all_cards_pricing_bool_exp = {}) {
        lotr_all_cards_pricing_aggregate(where: $where) {
          aggregate {
            count
          }
        }
      }
    `,
    {
      variables: {
        where: {
          _or: {
            ...queryFilters,
          },
        },
      },
    }
  );
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
  const { data, error, loading } = useSubscription(
    gql`
      subscription (
        $where: lotr_all_cards_pricing_bool_exp
        $order_by: [lotr_all_cards_pricing_order_by!]
        $limit: Int
        $offset: Int
      ) {
        lotr_all_cards_pricing: lotr_all_cards_pricing(
          where: $where
          order_by: $order_by
          limit: $limit
          offset: $offset
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
            ...queryFilters,
          },
        },
        order_by: { card_price: orderBy },
        limit: limitItems,
        offset: limitItems * page - limitItems,
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
        <Grid
          container
          spacing={1}
          item
          sm={isFilterOpen ? 10 : 12}
          sx={{ mt: 1 }}
        >
          <Grid item sm={10}>
            {paginationCountQuery.data?.lotr_all_cards_pricing_aggregate && (
              <Typography variant="subtitle2">
                {
                  paginationCountQuery.data?.lotr_all_cards_pricing_aggregate
                    .aggregate.count
                }{" "}
                items
              </Typography>
            )}
          </Grid>
          <Grid item sm={2}>
            <Select
              fullWidth
              size="small"
              value={limitItems}
              onChange={(e) => setLimitItems(e.target.value)}
            >
              <MenuItem value={10}>10</MenuItem>
              <MenuItem value={20}>20</MenuItem>
              <MenuItem value={50}>50</MenuItem>
            </Select>
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
          {loading &&
            Array.from({ length: limitItems }).map((i) => (
              <Grid item sm={2}>
                <Card>
                  <Skeleton variant="rounded" width={210} height={240} />
                  <CardContent>
                    <Typography gutterBottom variant="subtitle2" noWrap>
                      <Skeleton variant="text" sx={{ fontSize: "1rem" }} />
                    </Typography>
                    <Typography gutterBottom variant="subtitle2" noWrap>
                      <Skeleton variant="text" sx={{ fontSize: "1rem" }} />
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
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
          <Grid item sm={12} sx={{ display: "flex", justifyContent: "center" }}>
            {paginationCountQuery?.data && (
              <Pagination
                count={Math.ceil(
                  paginationCountQuery.data?.lotr_all_cards_pricing_aggregate
                    .aggregate.count / limitItems
                )}
                page={page}
                onChange={handlePageChange}
              />
            )}
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default IndexPage;
