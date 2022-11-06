import * as React from "react";

export const TcgIcon = ({ tcg }) => {
  return (
    <>
      {tcg === "hs" && (
        <img src="https://i.imgur.com/mWlj4DN.png" height="29px" width="106" />
      )}
      {tcg === "lotr" && (
        <img src="https://i.imgur.com/KHXNRx3.png" height="30px" />
      )}
      {tcg === "mtg" && (
        <img src="https://i.imgur.com/nzgIiXC.png" height="30px" />
      )}
      {tcg === "pokemon" && (
        <img src="https://i.imgur.com/9kK9giw.png" height="30px" width="106" />
      )}
      {tcg === "yugioh" && (
        <img src="https://i.imgur.com/nqpLbCj.png" height="30px" width="106" />
      )}
      {tcg === "fnb" && (
        <img src="https://i.imgur.com/iSjXh55.png" height="30px" width="106" />
      )}
    </>
  );
};
