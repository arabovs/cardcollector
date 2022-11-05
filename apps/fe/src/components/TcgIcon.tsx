import * as React from "react";

export const TcgIcon = ({ tcg }) => {
  return (
    <>
      {tcg === "hearthstore" && (
        <img src="https://i.imgur.com/wy4NPtt.png" height="30px" />
      )}
      {tcg === "lotr" && (
        <img src="https://i.imgur.com/ccNQNgR.png" height="30px" />
      )}
      {tcg === "mtg" && (
        <img
          src="https://imgur.com/gallery/cEGBppR"
          height="30px"
          width="30px"
        />
      )}
      {tcg === "pokemon" && (
        <img src="https://i.imgur.com/KJHBOBk.png" height="30px" />
      )}
      {tcg === "yugioh" && (
        <img src="https://i.imgur.com/UzBdphZ.png" height="30px" />
      )}
    </>
  );
};
