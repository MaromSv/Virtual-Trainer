-- Up

CREATE TABLE User (
  id INTEGER PRIMARY KEY,
  username STRING,
  password STRING
);

-- Down

DROP TABLE User;