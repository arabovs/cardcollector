import * as React from "react";

export const TcgIcon = ({ tcg }) => {
  return (
    <>
      {tcg === "hearthstone" && (
        <img src="https://i.imgur.com/8oUe1kX.png" height="40px" />
      )}
      {tcg === "lotr" && (
        <img src="https://i.imgur.com/KHXNRx3.png" height="30px" />
      )}
      {tcg === "mtg" && (
        <img src="https://i.imgur.com/nzgIiXC.png" height="30px" />
      )}
      {tcg === "pokemon" && (
        <img src="https://i.imgur.com/wWSijOI.png" height="30px" />
      )}
      {tcg === "yugioh" && (
        <img src="https://i.imgur.com/0ktEksU.png" height="45px" />
      )}
    </>
  );
};
