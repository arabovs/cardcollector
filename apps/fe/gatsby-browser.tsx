import React from "react";
import { Navigation } from "./src/gatsby-theme-material-ui-top-layout/components/top-layout";

const SelectedGameContext = React.createContext(null);

export const useSelectedGameContext = () => {
  const selected = React.useContext(SelectedGameContext);
  return selected;
};

const SelectedGameProvider = ({ children, game }) => {
  return (
    <SelectedGameContext.Provider value={game}>
      {children}
    </SelectedGameContext.Provider>
  );
};

export const wrapPageElement = ({ element, props }) => {
  const { game } = props.params;
  return (
    <SelectedGameProvider game={game}>
      <Navigation game={game}>{element}</Navigation>
    </SelectedGameProvider>
  );
};
