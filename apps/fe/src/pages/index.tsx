import { useSubscription, gql, useQuery } from "@apollo/client";
import {
  Box,
  Button,
  Card,
  CardContent,
  Checkbox,
  Chip,
  Collapse,
  FormControl,
  Grid,
  IconButton,
  InputAdornment,
  InputLabel,
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
import { useGameSelectorContext } from "../gatsby-theme-material-ui-top-layout/components/top-layout";
import { GameCard } from "../components/GameCard";
import labels from "./../constants/labels.json";

export const filter_type_label = {
  set: {
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
  const [searchKeyword, setSearchKeyWord] = useState("");
  return (
    <>
      <ListItemButton onClick={() => setFilterTypeOpen((p) => !p)}>
        <ListItemText primary={filterName} />
        <Typography variant="caption" sx={{ mr: 1 }}>
          {filters.length}
        </Typography>
        {isFilterTypeOpen ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Collapse in={isFilterTypeOpen} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <ListItem sx={{ pl: 4 }}>
            <TextField
              variant="outlined"
              placeholder="Search"
              size="small"
              fullWidth
              value={searchKeyword}
              onChange={(e) => setSearchKeyWord(e.target.value)}
            />
          </ListItem>
          {filters
            .filter((type) => {
              return String(type.value)
                ?.toLowerCase()
                ?.includes(searchKeyword.toLowerCase());
            })
            .map((type) => (
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
                <ListItemText
                  primary={
                    (filter_type_label[type.key] &&
                      filter_type_label[type.key][type.value]) ||
                    type.value
                  }
                  primaryTypographyProps={{ noWrap: true }}
                />
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
  const [selectedFilters, setSelectedFilters] = useState([]);
  const [orderBy, setOrderBy] = useState(null);
  const [limitItems, setLimitItems] = useState(48);
  const [page, setPage] = React.useState(1);
  const handlePageChange = (event, value: number) => {
    setPage(value);
  };
  const { selectedGame } = useGameSelectorContext();
  useEffect(() => {
    setSelectedFilters([]);
  }, [selectedGame]);
  const filterTypesQuery = useQuery(
    gql`
      query FilterTypes($tcg: String_comparison_exp!) {
        type: card_generic(
          distinct_on: type
          where: { tcg: $tcg, type: { _is_null: false } }
        ) {
          type
        }
        subtype: card_generic(
          distinct_on: subtype
          where: { tcg: $tcg, subtype: { _is_null: false } }
        ) {
          subtype
        }
        kind: card_generic(
          distinct_on: kind
          where: { tcg: $tcg, kind: { _is_null: false } }
        ) {
          kind
        }
        cost: card_generic(
          distinct_on: cost
          where: { tcg: $tcg, cost: { _is_null: false } }
        ) {
          cost
        }
        attack: card_generic(
          distinct_on: attack
          where: { tcg: $tcg, attack: { _is_null: false } }
        ) {
          attack
        }
        defence: card_generic(
          distinct_on: defence
          where: { tcg: $tcg, defence: { _is_null: false } }
        ) {
          defence
        }
        set: card_generic(
          distinct_on: set
          where: { tcg: $tcg, set: { _is_null: false } }
        ) {
          set
        }
        rarity: card_generic(
          distinct_on: rarity
          where: { tcg: $tcg, rarity: { _is_null: false } }
        ) {
          rarity
        }
      }
    `,
    { variables: { tcg: { _eq: selectedGame } } }
  );
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
      query PaginationCount($where: card_generic_bool_exp = {}) {
        card_generic_aggregate(where: $where) {
          aggregate {
            count
          }
        }
      }
    `,
    {
      variables: {
        where: {
          name: { _ilike: `%${searchField}%` },
          tcg: { _eq: selectedGame },
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
  )
    .filter(([_, value]) => value.length !== 0)
    .map(([key, value]) => ({
      key,
      label: labels[selectedGame][key],
      values: value.map((item) => ({
        key,
        value: item[key],
        label: labels[selectedGame][key],
      })),
    }));

  const { data, error, loading } = useSubscription(
    gql`
      subscription (
        $where: card_generic_bool_exp
        $order_by: [card_generic_order_by!]
        $limit: Int
        $offset: Int
      ) {
        card_generic(
          where: $where
          order_by: $order_by
          limit: $limit
          offset: $offset
        ) {
          id
          name
          price
          set
          image
        }
      }
    `,
    {
      variables: {
        where: {
          name: { _ilike: `%${searchField}%` },
          tcg: { _eq: selectedGame },
          _or: {
            ...queryFilters,
          },
        },
        order_by: { price: orderBy },
        limit: limitItems,
        offset: limitItems * page - limitItems,
      },
    }
  );
  if (error) return <div>{error.message}</div>;
  return (
    <Box sx={{ mt: 2, mb: 2, pl: 1, pr: 1 }}>
      <Grid container spacing={1}>
        <Grid
          item
          xs={8}
          sm={10}
          sx={{ display: "flex", alignItems: "center" }}
        >
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
        <Grid item xs={4} sm={2}>
          <FormControl fullWidth size="small">
            <InputLabel id="demo-simple-select-label">Sort</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              label="Sort"
              fullWidth
              size="small"
              value={orderBy}
              onChange={(e) => setOrderBy(e.target.value)}
              endAdornment={
                orderBy && (
                  <InputAdornment position="end" sx={{ mr: 1 }}>
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
          </FormControl>
        </Grid>
      </Grid>
      <Grid container spacing={1} sx={{ mt: 1 }}>
        {isFilterOpen && (
          <Grid item xs={12} sm={4} md={3} lg={2} xl={1.5}>
            <Card
              variant="outlined"
              sx={{ maxHeight: "90vh", overflowY: "auto" }}
            >
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
          xs={12}
          sm={isFilterOpen ? 8 : 12}
          md={isFilterOpen ? 9 : 12}
          lg={isFilterOpen ? 10 : 12}
          xl={isFilterOpen ? 10.5 : 12}
        >
          <Grid item sm={10}>
            {paginationCountQuery.data?.card_generic_aggregate && (
              <Typography variant="subtitle2">
                {
                  paginationCountQuery.data?.card_generic_aggregate.aggregate
                    .count
                }{" "}
                items
              </Typography>
            )}
          </Grid>
          <Grid item sm={2}>
            <FormControl fullWidth size="small">
              <InputLabel id="show_number">Show number</InputLabel>
              <Select
                labelId="show_number"
                fullWidth
                size="small"
                value={limitItems}
                onChange={(e) => setLimitItems(e.target.value)}
                label="Show number"
              >
                <MenuItem value={10}>10</MenuItem>
                <MenuItem value={20}>20</MenuItem>
                <MenuItem value={50}>50</MenuItem>
              </Select>
            </FormControl>
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
              <Grid item xs={6} md={3} xl={1.5}>
                <Card variant="outlined">
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
          {data?.card_generic.map((item) => (
            <Grid item xs={6} md={3} xl={1.5} key={item.id}>
              <GameCard
                id={item.id}
                image={item.image}
                name={item.name}
                set={item.set}
              />
            </Grid>
          ))}
          <Grid item sm={12} sx={{ display: "flex", justifyContent: "center" }}>
            {paginationCountQuery?.data && (
              <Pagination
                count={Math.ceil(
                  paginationCountQuery.data?.card_generic_aggregate.aggregate
                    .count / limitItems
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
