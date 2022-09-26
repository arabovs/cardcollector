import React from "react";
import { Link } from "gatsby";
import { Box, Grid, TextField, Typography } from "@mui/material";
import { SetComponent } from "../components/SetComponent";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";

const SearchPage = () => {
  const [value, setValue] = React.useState("Promotional");

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  return (
    <>
      <Link to="/">Go to Main</Link>
      <div>
        <Box sx={{ minWidth: 120 }}>
          <FormControl fullWidth>
            Card Set:
            <Select
              labelId="edition-selector"
              id="edition-selector"
              value={value}
              label="edition-selector"
              onChange={handleChange}
              maxWidth={100}
            >
              <MenuItem value="Promotional">Promotional</MenuItem>
              <MenuItem value="The-Fellowship-of-the-Ring">
                The Fellowship of the Ring
              </MenuItem>
              <MenuItem value="Mines-of-Moria">Mines of Moria</MenuItem>
              <MenuItem value="Realms-of-the-Elf-lords">
                Realms of the Elf-lords
              </MenuItem>
              <MenuItem value="The-two-Towers">The two Towers</MenuItem>
              <MenuItem value="Battle-of-helms-Deep">
                Battle of Helm's Deep
              </MenuItem>
              <MenuItem value="Ents-of-Fangorn">Ents of Fangorn</MenuItem>
              <MenuItem value="The-Return-of-the-King">
                The Return of the King
              </MenuItem>
              <MenuItem value="Siege-of-Gondor">Siege of Gondor</MenuItem>
              <MenuItem value="Reflections">Reflections</MenuItem>
              <MenuItem value="Mount-Doom">Mount Doom</MenuItem>
              <MenuItem value="Shadows">Shadows</MenuItem>
              <MenuItem value="Black-Rider">Black Rider</MenuItem>
              <MenuItem value="Bloodlines">Bloodlines</MenuItem>
              <MenuItem value="Expanded-Middle-earth">
                Expanded Middle-earth
              </MenuItem>
              <MenuItem value="The-Hunters">The Hunters</MenuItem>
              <MenuItem value="The-Wraith-Collection">
                The Wraith Collection
              </MenuItem>
              <MenuItem value="Rise-of-Saruman">Rise of Saruman</MenuItem>
              <MenuItem value="Treachery-and-Deceit">
                Treachery & Deceit
              </MenuItem>
            </Select>
          </FormControl>
        </Box>

        <SetComponent inputText={value} />
      </div>
    </>
  );
};

export default SearchPage;
