import React from "react";
//import { Button } from "grommet";
import { Box, Button, DropButton, Heading, Text } from 'grommet';

export const GrommetButton = () => {
  return (
    <div>
      <DropButton
        label="Set"
        dropContent={
          <Box>1</Box>
        }
      />
    </div>
  );
};
