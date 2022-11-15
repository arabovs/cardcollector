import { useSubscription, gql } from "@apollo/client";
import { Container, Grid } from "@mui/material";
import { Link } from "gatsby";
import React from "react";
import { TcgIcon } from "../components/TcgIcon";

const IndexPage = () => {
  const { data, loading, error } = useSubscription(gql`
    subscription GamesQueryIndex {
      card_details(distinct_on: tcg) {
        tcg
      }
    }
  `);

  if (loading) return null;
  if (error) return <div>{error.message}</div>;

  return (
    <Container
      sx={{
        mt: 2,
        mb: 2,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Grid container spacing={5}>
        {data.card_details.map(({ tcg }) => (
          <Grid item xs={12} sm={6} md={4}>
            <Link to={`${tcg}`}>
              <TcgIcon tcg={tcg} width="100%"></TcgIcon>
            </Link>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default IndexPage;
