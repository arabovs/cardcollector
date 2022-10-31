import { gql, useQuery } from "@apollo/client";
import {
  AutoStories,
  Dashboard,
  ExpandLess,
  ExpandMore,
  Favorite,
  FavoriteBorderOutlined,
  FormatListBulleted,
  Label,
  LocalOffer,
  Numbers,
  Report,
  Share,
  Timeline,
} from "@mui/icons-material";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Collapse,
  Container,
  Divider,
  Grid,
  IconButton,
  Typography,
} from "@mui/material";
import { brown, purple, red } from "@mui/material/colors";
import { alpha, Box } from "@mui/system";
import React, { useState } from "react";
import { filter_type_label } from "..";

const CardPage = (props) => {
  const { id } = props.params;
  const [isPropertiesOpen, setPropertiesOpen] = useState(true);
  const [isStatsOpen, setStatsOpen] = useState(true);
  const { data, loading, error } = useQuery(
    gql`
      query CardById($id: uuid!) {
        lotr_all_cards_pricing_by_pk(id: $id) {
          id
          card_img
          card_name
          lore
          card_price
          type
          kind
          culture
          set
          rarity
          signet
          card_id
          text
          twilight
          strength
          vitality
          resistance
        }
      }
    `,
    { variables: { id } }
  );
  if (error) return <div>{error.message}</div>;
  return (
    <Container sx={{ mt: 2, mb: 2 }}>
      <Grid container spacing={2}>
        <Grid item sm={5}>
          {data && (
            <>
              <Card variant="outlined">
                <CardContent>
                  <Box display="flex" justifyContent={"flex-end"}>
                    <IconButton size="small" sx={{ mb: 1 }}>
                      <FavoriteBorderOutlined fontSize="small" />
                    </IconButton>
                  </Box>
                  <img
                    src={data?.lotr_all_cards_pricing_by_pk.card_img}
                    style={{ width: "100%" }}
                  />
                </CardContent>
              </Card>
              <Card variant="outlined" sx={{ mt: 2 }}>
                <CardHeader title="Text" avatar={<AutoStories />} />
                <Divider />
                <CardContent>
                  <Typography gutterBottom>
                    {data?.lotr_all_cards_pricing_by_pk.text}
                  </Typography>
                  <Typography variant="body2" sx={{ fontStyle: "italic" }}>
                    {data?.lotr_all_cards_pricing_by_pk.lore}
                  </Typography>
                </CardContent>
                <Divider />
                <CardHeader
                  title="Properties"
                  avatar={<Label />}
                  action={
                    <IconButton onClick={() => setPropertiesOpen((p) => !p)}>
                      {!isPropertiesOpen ? <ExpandMore /> : <ExpandLess />}
                    </IconButton>
                  }
                />
                <Collapse in={isPropertiesOpen}>
                  <Divider />
                  <CardContent>
                    <Grid container display="flex" spacing={1}>
                      <Grid item sm={4}>
                        <Card
                          sx={{
                            p: 1,
                            backgroundColor: "rgba(25,118,210,0.1)",
                            borderColor: "primary.main",
                          }}
                          variant="outlined"
                        >
                          <Typography
                            textAlign={"center"}
                            component="div"
                            variant="caption"
                            gutterBottom
                            color="primary"
                          >
                            Тype
                          </Typography>
                          <Typography textAlign={"center"}>
                            {data?.lotr_all_cards_pricing_by_pk.type}
                          </Typography>
                        </Card>
                      </Grid>
                      <Grid item sm={4}>
                        <Card
                          sx={{
                            p: 1,
                            backgroundColor: "rgba(25,118,210,0.1)",
                            borderColor: "primary.main",
                          }}
                          variant="outlined"
                        >
                          <Typography
                            textAlign={"center"}
                            component="div"
                            variant="caption"
                            gutterBottom
                            color="primary"
                          >
                            Kind
                          </Typography>
                          <Typography textAlign={"center"}>
                            {data?.lotr_all_cards_pricing_by_pk.kind}
                          </Typography>
                        </Card>
                      </Grid>
                      <Grid item sm={4}>
                        <Card
                          sx={{
                            p: 1,
                            backgroundColor: "rgba(25,118,210,0.1)",
                            borderColor: "primary.main",
                          }}
                          variant="outlined"
                        >
                          <Typography
                            textAlign={"center"}
                            component="div"
                            variant="caption"
                            gutterBottom
                            color="primary"
                          >
                            Culture
                          </Typography>
                          <Typography textAlign={"center"}>
                            {data?.lotr_all_cards_pricing_by_pk.culture}
                          </Typography>
                        </Card>
                      </Grid>
                      <Grid item sm={4}>
                        <Card
                          sx={{
                            p: 1,
                            backgroundColor: "rgba(25,118,210,0.1)",
                            borderColor: "primary.main",
                          }}
                          variant="outlined"
                        >
                          <Typography
                            textAlign={"center"}
                            component="div"
                            variant="caption"
                            gutterBottom
                            color="primary"
                          >
                            Set
                          </Typography>
                          <Typography textAlign={"center"} noWrap>
                            {
                              filter_type_label["set"][
                                data?.lotr_all_cards_pricing_by_pk.set
                              ]
                            }
                          </Typography>
                        </Card>
                      </Grid>
                      <Grid item sm={4}>
                        <Card
                          sx={{
                            p: 1,
                            backgroundColor: "rgba(25,118,210,0.1)",
                            borderColor: "primary.main",
                          }}
                          variant="outlined"
                        >
                          <Typography
                            textAlign={"center"}
                            component="div"
                            variant="caption"
                            gutterBottom
                            color="primary"
                          >
                            Rarity
                          </Typography>
                          <Typography textAlign={"center"}>
                            {
                              filter_type_label["rarity"][
                                data?.lotr_all_cards_pricing_by_pk.rarity
                              ]
                            }
                          </Typography>
                        </Card>
                      </Grid>
                      {data?.lotr_all_cards_pricing_by_pk.signet && (
                        <Grid item sm={4}>
                          <Card
                            sx={{
                              p: 1,
                              backgroundColor: "rgba(25,118,210,0.1)",
                              borderColor: "primary.main",
                            }}
                            variant="outlined"
                          >
                            <Typography
                              textAlign={"center"}
                              component="div"
                              variant="caption"
                              gutterBottom
                              color="primary"
                            >
                              Signet
                            </Typography>
                            <Typography textAlign={"center"}>
                              {data?.lotr_all_cards_pricing_by_pk.signet}
                            </Typography>
                          </Card>
                        </Grid>
                      )}
                    </Grid>
                  </CardContent>
                </Collapse>
                <Divider />
                <CardHeader
                  title="Stats"
                  avatar={<Numbers />}
                  action={
                    <IconButton onClick={() => setStatsOpen((p) => !p)}>
                      {!isStatsOpen ? <ExpandMore /> : <ExpandLess />}
                    </IconButton>
                  }
                />
                <Collapse in={isStatsOpen}>
                  <Divider />
                  <CardContent>
                    <Grid container spacing={1}>
                      {data?.lotr_all_cards_pricing_by_pk.twilight && (
                        <Grid item sm={4}>
                          <Card
                            sx={{
                              p: 1,
                              backgroundColor: "rgba(25,118,210,0.1)",
                              borderColor: "primary.main",
                            }}
                            variant="outlined"
                          >
                            <Typography
                              textAlign={"center"}
                              component="div"
                              variant="caption"
                              gutterBottom
                              color="primary"
                            >
                              Twilight
                            </Typography>
                            <Typography textAlign={"center"}>
                              {data?.lotr_all_cards_pricing_by_pk.twilight}
                            </Typography>
                          </Card>
                        </Grid>
                      )}
                      {data?.lotr_all_cards_pricing_by_pk.strength && (
                        <Grid item sm={4}>
                          <Card
                            sx={{
                              p: 1,
                              backgroundColor: alpha(brown[500], 0.1),
                              borderColor: brown[500],
                            }}
                            variant="outlined"
                          >
                            <Typography
                              textAlign={"center"}
                              component="div"
                              variant="caption"
                              gutterBottom
                              color={brown[500]}
                            >
                              Strength
                            </Typography>
                            <Typography textAlign={"center"}>
                              {data?.lotr_all_cards_pricing_by_pk.strength}
                            </Typography>
                          </Card>
                        </Grid>
                      )}
                      {data?.lotr_all_cards_pricing_by_pk.vitality && (
                        <Grid item sm={4}>
                          <Card
                            sx={{
                              p: 1,
                              backgroundColor: alpha(red[500], 0.1),
                              borderColor: red[500],
                            }}
                            variant="outlined"
                          >
                            <Typography
                              textAlign={"center"}
                              component="div"
                              variant="caption"
                              gutterBottom
                              color={red[500]}
                            >
                              Vitality
                            </Typography>
                            <Typography textAlign={"center"}>
                              {data?.lotr_all_cards_pricing_by_pk.vitality}
                            </Typography>
                          </Card>
                        </Grid>
                      )}
                      {data?.lotr_all_cards_pricing_by_pk.resistance && (
                        <Grid item sm={4}>
                          <Card
                            sx={{
                              p: 1,
                              backgroundColor: alpha(purple[500], 0.1),
                              borderColor: purple[500],
                            }}
                            variant="outlined"
                          >
                            <Typography
                              textAlign={"center"}
                              component="div"
                              variant="caption"
                              gutterBottom
                              color={purple[500]}
                            >
                              Resistance
                            </Typography>
                            <Typography textAlign={"center"}>
                              {data?.lotr_all_cards_pricing_by_pk.resistance}
                            </Typography>
                          </Card>
                        </Grid>
                      )}
                    </Grid>
                  </CardContent>
                </Collapse>
              </Card>
            </>
          )}
        </Grid>
        <Grid item sm={7}>
          <Card variant="outlined">
            <CardHeader
              title={`${data?.lotr_all_cards_pricing_by_pk.card_name} (#${
                data?.lotr_all_cards_pricing_by_pk.card_id
              }) ${
                filter_type_label["set"][data?.lotr_all_cards_pricing_by_pk.set]
              }`}
              action={
                <>
                  <IconButton size="small" sx={{ mb: 1 }}>
                    <Share fontSize="small" />
                  </IconButton>
                  <IconButton size="small" sx={{ mb: 1 }}>
                    <Report fontSize="small" />
                  </IconButton>
                </>
              }
            />
            <CardContent>
              <Box sx={{ mb: 2 }}>
                Current price <br />{" "}
                <Typography variant="h4">
                  {new Intl.NumberFormat("en-US", {
                    style: "currency",
                    currency: "USD",
                  }).format(data?.lotr_all_cards_pricing_by_pk.card_price)}
                </Typography>
              </Box>
              <Grid container spacing={2}>
                <Grid item sm={6}>
                  <Button fullWidth variant="contained">
                    add to cart
                  </Button>
                </Grid>
                <Grid item sm={6}>
                  <Button fullWidth variant="outlined">
                    make an offer
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
          <Card sx={{ mt: 2 }} variant="outlined">
            <CardHeader
              title={`Price history`}
              avatar={<Timeline />}
              action={
                <IconButton>
                  <ExpandMore />
                </IconButton>
              }
            />
          </Card>
          <Card sx={{ mt: 2 }} variant="outlined">
            <CardHeader
              title={`Listings`}
              avatar={<LocalOffer />}
              action={
                <IconButton>
                  <ExpandMore />
                </IconButton>
              }
            />
          </Card>
          <Card sx={{ mt: 2 }} variant="outlined">
            <CardHeader
              title={`Offers`}
              avatar={<FormatListBulleted />}
              action={
                <IconButton>
                  <ExpandMore />
                </IconButton>
              }
            />
          </Card>
        </Grid>
      </Grid>
      <Card sx={{ mt: 2 }} variant="outlined">
        <CardHeader
          title={`More cards like this one`}
          avatar={<Dashboard />}
          action={
            <IconButton>
              <ExpandMore />
            </IconButton>
          }
        />
      </Card>
    </Container>
  );
};

export default CardPage;
