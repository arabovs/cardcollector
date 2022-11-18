import * as React from "react";

export const TcgIcon = ({ tcg, width }) => {
  return (
    <>
      {tcg === "hs" && (
        <img
          src="https://i.imgur.com/mWlj4DN.png"
          {...(!width ? { height: "29px", width: "106" } : { width })}
        />
      )}
      {tcg === "lotr" && (
        <img
          src="https://i.imgur.com/KHXNRx3.png"
          {...(!width ? { height: "30px" } : { width })}
        />
      )}
      {tcg === "mtg" && (
        <img
          src="https://i.imgur.com/nzgIiXC.png"
          {...(!width ? { height: "30px" } : { width })}
        />
      )}
      {tcg === "pokemon" && (
        <img
          src="https://i.imgur.com/9kK9giw.png"
          {...(!width ? { height: "30px", width: "106" } : { width })}
        />
      )}
      {tcg === "yugioh" && (
        <img
          src="https://i.imgur.com/nqpLbCj.png"
          {...(!width ? { height: "30px", width: "106" } : { width })}
        />
      )}
      {tcg === "fnb" && (
        <img
          src="https://i.imgur.com/iSjXh55.png"
          {...(!width ? { height: "30px", width: "106" } : { width })}
        />
      )}
    </>
  );
};
